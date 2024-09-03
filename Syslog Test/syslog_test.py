#!/usr/bin/python3
import socket
import argparse
from datetime import datetime as dt
import json as js

# define enums
VR = "1.1.0"
AUTHOR = "UnderATK"

# define log level enum
LEVEL = {
    'emerg': 0, 'alert':1, 'crit': 2, 'err': 3,
    'warning': 4, 'notice': 5, 'info': 6, 'debug': 7
}

def syslog(message, level=LEVEL['info'], host='localhost', port=514, number=1, json=False):
    current_time = f"{dt.now().date()} {'{:02d}'.format(dt.now().hour)}:{'{:02d}'.format(dt.now().minute)}:{'{:02d}'.format(dt.now().second)}"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = socket.gethostname()
    s_ip = socket.gethostbyname(hostname)
    d_ip = socket.gethostbyname(host)

    if json:
        data = f'{{"log_level":"{level}","timestamp":"{current_time}","hostname":"{hostname}","source_ip":"{s_ip}","destination_ip":"{d_ip}","msg":"{message}"}}'
        data = js.loads(data)
    else:
        data = f"<{level}> {current_time} {hostname} source_ip={s_ip} destination_ip={d_ip} msg={message}\n"

    if number > 1:
        for _ in range(1,number+1):
            sock.sendto(data.encode(), (host, port))
    else:
        sock.sendto(data.encode(), (host, port))
    sock.close()

# Welcome banner
print("-" * 50)
print(f"-----\tSyslog Tester")
print(f"-----\tBy {AUTHOR}")
print("-" * 50)

parser = argparse.ArgumentParser(
    prog="Syslog Tester",
    description="Syslog Tester checking logging to host.",
    usage="python3 syslog_test.py [-h] [-m MESSAGE] [-l LEVEL] [-H HOST] [-p PORT] [-n NUMBER] [--version]",
    epilog="Get the best of your service! For any additional needs for this script please feel free to contact me.")
parser.add_argument('-m', "--message", help="Syslog message.", type=str, default="syslog test message")
parser.add_argument('-l', "--level", help="Syslog level: emergency=0 alert=1 critical=2 error=3 warning=4 notice=5 info=6 debug=7", type=int, default=6)
parser.add_argument('-H', "--host", help="Remote syslog server ip.", default="localhost")
parser.add_argument('-p', "--port", help="Remote syslog server port.", type=int, default=514)
parser.add_argument('-n', "--number", help="Number of messages to send.", type=int, default=1)
parser.add_argument('-j', "--json", help="Use JSON log format.", action="store_true")
parser.add_argument("--version", action="version", version="%(prog)s - Version {}".format(VR))
args = parser.parse_args()

syslog(message=args.message, level=args.level, host=args.host, port=args.port, number=args.number, json=args.json)
