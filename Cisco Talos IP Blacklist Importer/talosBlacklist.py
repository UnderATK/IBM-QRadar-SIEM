#!/usr/bin/python3
import json
import requests
import urllib3
import argparse

# define enums
VR = "1.0.0"
AUTHOR = "UnderATK"

# Token
token = ""

# URL
qradarUrl = ""

# Header
qradarHeaders = {"SEC": token}

# Reference Set - 'Talos IP Blacklist'
path = "/api/reference_data/sets/bulk_load/Talos%2520IP%2520Blacklist"
deletePath = "/api/reference_data/sets/Talos%2520IP%2520Blacklist?purge_only=true"

urllib3.disable_warnings() # disable warnings

def getData():
    ipArray = []
    http = "https://talosintelligence.com/documents/ip-blacklist"
    response = requests.get(http)
    data = response.text
    data = data.replace("\n", ",")
    
    for x in data.split(","):
        ipArray.append(x)
    
    ipArray = list(filter(None, ipArray)) # remove empty strings from the list.
    return ipArray

def importer():
    ipArray = getData()
    try:
        print("Connecting to QRadar API -")
        json_delete = requests.delete(qradarUrl + deletePath, headers=qradarHeaders, verify=False, timeout=10)
        httpResponseDelete = json_delete.status_code
        if (httpResponseDelete == 200):
            print("\033[01m\033[32mOK\033[0m", end="")
            print("Reference Set 'Talos IP Blacklist' purged successfully.")
            json_data = requests.post(qradarUrl + path, headers=qradarHeaders, data=json.dumps(ipArray), verify=False, timeout=10)
            httpResponseAdd = json_data.status_code
            if (httpResponseAdd == 200):
                print("\033[01m\033[32mOK\033[0m")
                print("Data added successfully to 'Talos IP Blacklist' Reference Set.")
            else:
                print(f"\033[01m\033[31mError\033[0m - status code: {httpResponseAdd}")
        else:
            print(f"\033[01m\033[31mError\033[0m - status code: {httpResponseDelete}")
    
    except Exception as e:
        print(f"\033[01m\033[31mError\033[0m - {e}")

# Welcome Banner
print("-" * 50)
print(f"-----\tCisco Talos IP Blacklist Importer")
print(f"-----\tBy {AUTHOR}")
print("-" * 50)

parser = argparse.ArgumentParser(
    prog="Cisco Talos IP Blacklist Importer",
    description="This program will update the reference set of Talos IP Blacklist.\n"
    "Supported QRadar API versions: <16.0",
    usage="python3 talosBlacklist.py [-h] [--version]",
    epilog="Get the best of your service! For any additional needs for this script please feel free to contact me.",
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--version", action="version", version="%(prog)s - Version {}".format(VR))
args = parser.parse_args()

importer()
