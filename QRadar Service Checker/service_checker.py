#/bin/python3
import subprocess
import argparse
from datetime import datetime as dt

# define enums
VR = "0.1.0"
AUTHOR = "UnderATK"

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
                 "iptables":{"err":"iptables Firewall is not running"}}

#systemctl is-active <service>'
def checker(host='localhost'):
    print("-" * 50)
    print(f"Checking services on host: {host}")
    print("-" * 50)

    if host != 'localhost':
        command = f"systemctl --host root@{host} is-active "
    else:
        command = "systemctl is-active "

    for srv in services_dict:
        result = subprocess.run(command+srv, shell=True, capture_output=True)
        status = result.stdout.decode().strip('\n')

        if status == 'active':
            print(f"Service '{srv}' is {GRN_TXT + status + WHITE_TXT}")
        elif status == 'inactive':
            print(f"Service '{srv}' is {GREY_TXT + status + WHITE_TXT} - {GREY_TXT}service not running{WHITE_TXT}")
        elif status == 'failed':
            print(f"Service '{srv}' is {ERR_TXT + status + WHITE_TXT} - {ERR_TXT + services_dict.get(srv).get('err') + WHITE_TXT}")

# Welcome banner
print("-" * 50)
print(f"-----\tQRadar Service Checker v{VR}")
print(f"-----\tBy {AUTHOR}")
print("-" * 50)

parser = argparse.ArgumentParser(usage="python3 service_checker.py [-h] [-H HOST_IP]")
parser.add_argument('-H', "--host", help="Host ip.", default="localhost")
args = parser.parse_args()

checker(host=args.host)
