#/usr/bin/python3
import argparse
import csv
import subprocess
from datetime import datetime as dt
from colorama import Fore, Style, init
import os

# Initialize colorama for colored terminal output
init(autoreset=True)

# Dictionary with service error messages and possible fixes
services_dict = {
    "hostcontext": {
        "err": "Hostcontext manages all other services except ecs-ingress. All services controlled by hostcontext will be inactive until restarted.",
        "fix": "Restart the hostcontext service using the command: 'systemctl restart hostcontext'."
    },
    "hostservices": {
        "err": "The database and IMQ stop working, which also impacts hostcontext and tomcat.",
        "fix": "Check the database status: 'systemctl status database'. Restart hostservices and IMQ using 'systemctl restart hostservices' and 'systemctl restart imq'."
    },
    "tomcat": {
        "err": "The UI will be unavailable.",
        "fix": "Restart the tomcat service: 'systemctl restart tomcat'."
    },
    "ecs-ep": {
        "err": "This impacts data processing.",
        "fix": "Restart the ecs-ep service using: 'systemctl restart ecs-ep'."
    },
    "ecs-ec": {
        "err": "Parsing and normalizing events and flows will stop.",
        "fix": "Restart the ecs-ec service: 'systemctl restart ecs-ec'."
    },
    "ecs-ec-ingress": {
        "err": "When stopped, it prevents events from being collected in a buffer and spooled to other ecs services.",
        "fix": "Restart ecs-ec-ingress using: 'systemctl restart ecs-ec-ingress'. Ensure that there is enough space in the spool directory."
    },
    "ariel_proxy_server": {
        "err": "All requests to managed hosts for data from searches will stop until this server restarts.",
        "fix": "Restart the ariel_proxy_server: 'systemctl restart ariel_proxy_server'. Check the network connection between managed hosts and QRadar."
    },
    "ariel_query_server": {
        "err": "All searches of the Ariel database on managed hosts will stop.",
        "fix": "Restart the ariel_query_server: 'systemctl restart ariel_query_server'. Ensure that the Ariel database is functioning properly."
    },
    "asset_profiler": {
        "err": "Assets will not be added or updated until this service is back online.",
        "fix": "Restart the asset_profiler service: 'systemctl restart asset_profiler'. Verify asset profiler configurations and the asset database."
    },
    "historical_correlation_server": {
        "err": "This impacts historical searches on offense data.",
        "fix": "Restart the historical_correlation_server: 'systemctl restart historical_correlation_server'. Check for any database corruption and disk space issues."
    },
    "reporting_executor": {
        "err": "All running reports will be canceled and need to be restarted. New scheduled reports will not run until this service is started.",
        "fix": "Restart the reporting_executor service: 'systemctl restart reporting_executor'. Verify that scheduled reports are properly configured."
    },
    "iptables": {
        "err": "The iptables firewall is not running, which can impact connections between hosts.",
        "fix": "Start or restart the iptables service: 'systemctl restart iptables'. Ensure that firewall rules are correctly set for host communication."
    },
    "postfix": {
        "err": "This impacts mailing services from QRadar.",
        "fix": "Restart the postfix service: 'systemctl restart postfix'. Check the mail queue and configuration settings."
    },
    "syslog-ng": {
        "err": "This impacts system logging on the host.",
        "fix": "Restart the syslog-ng service: 'systemctl restart syslog-ng'. Ensure that log files are being written to the correct directories."
    },
    "sshd": {
        "err": "This impacts SSH access to the host.",
        "fix": "Restart the SSH daemon: 'systemctl restart sshd'. Verify the SSH configuration and network access to the host."
    },
    "httpd": {
        "err": "This impacts the web server.",
        "fix": "Restart the httpd service: 'systemctl restart httpd'. Ensure that the web server is configured correctly and the network is functioning."
    }
}

# define enums
VER = "1.0.0"
AUTHOR = "UnderATK"
COLUMNS = ["date", "host", "service_name", "status", "error_description", "possible_fix"]

def print_banner():
    print("-" * 50)
    print(f"\tQRadar Service Checker")
    print(f"\tA script to monitor and fix QRadar services.")
    print(f"\tBy {AUTHOR}")
    print("-" * 50)

def current_time():
    return f"{dt.now().date()} {'{:02d}'.format(dt.now().hour)}:{'{:02d}'.format(dt.now().minute)}:{'{:02d}'.format(dt.now().second)}"

def check_service_status(service, host):
    """Checks if a service is active, inactive, or failed."""
    try:
        # If host is not localhost, use systemctl with the --host option
        if host != "localhost":
            result = subprocess.run(['systemctl', '--host', f'root@{host}', 'is-active', service], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:
            result = subprocess.run(['systemctl', 'is-active', service], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()  # 'active', 'inactive', or 'failed'
    except Exception as e:
        print(f"Error checking {service} on {host}: {e}")
        return "unknown"

def report_service_status(service, details, host, fix=False, verbose=False):
    """Reports the status of a service and handles 'failed' and 'inactive' states differently."""
    date = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    status = check_service_status(service)

    # Prepare the output to be printed and returned
    if status == "failed":
        if verbose:
            print(f"{Fore.RED}\nService '{service}' has failed.")
            print(f"{Fore.RED}Error: {details['err']}")
            if fix:
                print(f"{Fore.YELLOW}Fix: {details['fix']}")
    elif status == "inactive":
        if verbose:
            print(f"{Fore.YELLOW}Service '{service}' is inactive.")
    else:
        if verbose:
            print(f"{Fore.GREEN}Service '{service}' is active.")

    # Return the status and details for later use
    return {
        "date": date,
        "host": host,
        "service_name": service,
        "status": status,
        "error_description": details['err'] if status == "failed" else "N/A",
        "possible_fix": details['fix'] if fix and status == "failed" else "N/A"
    }

def output_to_csv(service_data, csvfile_writer):
    """Writes service details to a CSV file."""
    csvfile_writer.writerow([
        service_data['date'],
        service_data['host'],
        service_data['service_name'],
        service_data['status'],
        service_data['error_description'],
        service_data['possible_fix']
    ])

def generate_csv_filename(host):
    """Generates a CSV filename in the format DDMMYYYY_HOSTNAME_services.csv."""
    date_str = dt.now().strftime("%d%m%Y")
    hostname = host.replace(".", "_")  # Replacing dots in the hostname to avoid issues
    return f"{date_str}_{hostname}_services.csv"

def main():
    print_banner()
    # Argument parser setup
    parser = argparse.ArgumentParser(
            prog="QRadar Service Checker",
            description="QRadar SIEM services checking on specific host",
            usage="python3 service_checker.py [-h] [-H HOST_IP] [-o] [-f] [-v] [--version]",
            epilog="Get the best of your service! For any additional needs for this script please feel free to contact me.")
    parser.add_argument('-H', "--host", help="Host IP.", default="localhost")
    parser.add_argument('-o', "--output", help="Output details to CSV.", action="store_true")
    parser.add_argument('-f', "--fix", help="Show possible fix.", action="store_true")
    parser.add_argument('-v', "--verbose", help="Verbose mode. Show details of each step.", action="store_true")
    parser.add_argument("--version", action="version", version="%(prog)s - Version {}".format(VER))
    args = parser.parse_args()

    results = []
    csv_filename = generate_csv_filename(args.host) if args.output else None

    print(f"Checking services on host: {args.host}")
    print(f"Checking time: {current_time()}")
    print("-" * 50)

    # Prepare CSV file if --output is provided
    if args.output:
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(COLUMNS)
            
            # Iterate through the services and write status to CSV
            for service, details in services_dict.items():
                service_data = report_service_status(service, details, args.host, fix=args.fix, verbose=args.verbose)
                output_to_csv(service_data, writer)
                results.append(service_data)
        # Inform the user about CSV file creation
        csv_path = os.path.abspath(csv_filename)
        print(f"{Fore.GREEN}Service status has been written to '{csv_filename}' at {csv_path}.")
    else:
        # Collect results without writing to CSV
        for service, details in services_dict.items():
            service_data = report_service_status(service, details, args.host, fix=args.fix, verbose=args.verbose)
            results.append(service_data)

    # If verbose is off, show the results summary at the end
    if not args.verbose:
        print(f"{Fore.BLUE}Service Status Summary:")
        for result in results:
            if result['status'] == "failed":
                print(f"{Fore.RED}Service '{result['service_name']}' has failed.")
                print(f"Error: {result['error_description']}")
                if args.fix:
                    print(f"Fix: {result['possible_fix']}")
            elif result['status'] == "inactive":
                print(f"{Fore.YELLOW}Service '{result['service_name']}' is inactive.")
            else:
                print(f"{Fore.GREEN}Service '{result['service_name']}' is active.")

main()
