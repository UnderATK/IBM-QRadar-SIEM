#/usr/bin/python3
import subprocess
import argparse
from datetime import datetime as dt
import time
import pandas as pd
import csv

# define enums
VR = "0.2.0"
AUTHOR = "UnderATK"
COLUMNS = ["date", "host", "service_name", "status", "error_description"]

# text coloring enums
WHITE_TXT = "\033[0m"
GREY_TXT = "\033[30m"
GRN_TXT = "\033[0;32m"
ERR_TXT = "\033[31m"

# define variables
services_dict = {"hostcontext":{"err":"hostcontext is the mannger for all the other services except ecs-ingress. all services control by hostcontext would be inactive untill they restarted"},
                 "hostservices":{"err":"the data base stops working as well as IMQ. this also impacts hostcontext and tomcat"}, 
                 "tomcat":{"err":"UI would not be available"}, 
                 "ecs-ep":{"err":"impact on processing data"}, 
                 "ecs-ec":{"err":"impacts parsing and normalizing events and flows would stop"}, 
                 "ecs-ec-ingress":{"err":"when stopped would not allow events to be collected in a buffer and spooled to the other ecs service"}, 
                 "ariel_proxy_server":{"err":"all requests to managed host for data from searches would stop until this server restarts"}, 
                 "ariel_query_server":{"err":"all searches of the ariel database would stop on the managed hosts"}, 
                 "asset_profiler":{"err":"assets would not be added or updated until this service came back online"}, 
                 "historical_correlation_server":{"err":"impacts historical searches on offense data"},
                 "reporting_executor":{"err":"all running reports would be cancaled and would need to be restared. new scheduled reports would not run untill this service starts"},
                 "iptables":{"err":"iptables Firewall is not running, can impact on connection between hosts"},
                 "postfix":{"err":"impacts on mailing services from the QRadar"},
                 "syslog-ng":{"err":"impacts on system logging on the host"},
                 "sshd":{"err":"impacts on SSH service to the host"},
                 "httpd":{"err":"impacts on web server"}}

def service_check(command, srv):
    return subprocess.run(command+srv, shell=True, capture_output=True)

def service_check_printer(status, srv):
    if status == 'active':
        return f"Service '{srv}' is {GRN_TXT + status + WHITE_TXT}"
    elif status == 'inactive':
        return f"Service '{srv}' is {GREY_TXT + status + WHITE_TXT} - {GREY_TXT}service not running{WHITE_TXT}"
    elif status == 'failed':
        return f"Service '{srv}' is {ERR_TXT + status + WHITE_TXT} - {ERR_TXT + services_dict.get(srv).get('err') + WHITE_TXT}"

def checker(host='localhost', output=False, verbose=False):
    current_time = f"{dt.now().date()} {'{:02d}'.format(dt.now().hour)}:{'{:02d}'.format(dt.now().minute)}:{'{:02d}'.format(dt.now().second)}"
    results = []

    print("-" * 50)
    print(f"Checking services on host: {host}")
    print(f"Checking time: {current_time}")
    print("-" * 50)

    if host != 'localhost':
        command = f"systemctl --host root@{host} is-active "
    else:
        command = "systemctl is-active "

    if output:
        CSV_FILE_NAME = f"Services-{host}-{current_time}.csv"
        csv_init(CSV_FILE_NAME)

    for srv in services_dict:
        result = service_check(command, srv)
        status = result.stdout.decode().strip('\n')

        if output:
            if status == 'active':
                add_entry(CSV_FILE_NAME, current_time, host, srv, status, "")
            elif status == 'inactive':
                add_entry(CSV_FILE_NAME, current_time, host, srv, status, "service not running")
            elif status == 'failed':
                add_entry(CSV_FILE_NAME, current_time, host, srv, status, services_dict.get(srv).get('err'))

        if verbose:
            print(service_check_printer(status, srv))
        else:
            results.append(service_check_printer(status, srv))

    if not verbose: 
        time.sleep(2)
        for x in results:
            print(x)

def csv_init(csv_name):
    try:
        pd.read_csv(csv_name)
    except FileNotFoundError:
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(csv_name, index=False)

def add_entry(csv_name, date, host, service_name, status, error_desc):
    new_entry = {
        "date": date,
        "host": host,
        "service_name": service_name,
        "status": status,
        "error_description": error_desc
    }

    with open(csv_name, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=COLUMNS)
        writer.writerow(new_entry)

# Welcome banner
print("-" * 50)
print(f"-----\tQRadar Service Checker")
print(f"-----\tBy {AUTHOR}")
print("-" * 50)

parser = argparse.ArgumentParser(
    prog="QRadar Service Checker",
    description="QRadar SIEM services checking on specific host",
    usage="python3 service_checker.py [-h] [-H HOST_IP] [-o] [-v] [--version]",
    epilog="Get the best of your service! For any additional needs for this script please feel free to contact me.")
parser.add_argument('-H', "--host", help="Host ip.", default="localhost")
parser.add_argument('-o', "--output", help="Output details to CSV.", action="store_true")
parser.add_argument('-v', "--verbose", help="Verbose the details to show on the screen for each step.", action="store_true")
parser.add_argument("--version", action="version", version="%(prog)s - Version {}".format(VR))
args = parser.parse_args()

checker(host=args.host,output=args.output,verbose=args.verbose)
