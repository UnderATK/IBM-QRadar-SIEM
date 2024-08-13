#!/bin/python3
import socket
import argparse
from datetime import datetime as dt

# define enums
VR = "0.1.0"
AUTHOR = "UnderATK"

# define log level enum
LEVEL = {
    'emerg': 0, 'alert':1, 'crit': 2, 'err': 3,
    'warning': 4, 'notice': 5, 'info': 6, 'debug': 7
}

def syslog(message, level=LEVEL['info'], host='localhost', port=514, number=1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = f"<{level}> {dt.now()} msg={message}\n"
    if number > 1:
        for n in range(1,number+1):
            sock.sendto(data.encode(), (host, port))
    else:
        sock.sendto(data.encode(), (host, port))
    sock.close()

# Welcome banner
print("-" * 50)
print(f"-----\tSyslog Test v{VR}")
print(f"-----\tBy {AUTHOR}")
print("-" * 50)

parser = argparse.ArgumentParser(usage="python3 syslog_test.py [-h] [-m MESSAGE] [-l LEVEL] [-H HOST] [-p PORT] [-n NUMBER]")
parser.add_argument('-m', "--message", help="Syslog message.", type=str, default="syslog test message")
parser.add_argument('-l', "--level", help="Syslog level: emergency=0 alert=1 critical=2 error=3 warning=4 notice=5 info=6 debug=7", type=int, default=6)
parser.add_argument('-H', "--host", help="Remote syslog server ip.", default="localhost")
parser.add_argument('-p', "--port", help="Remote syslog server port.", type=int, default=514)
parser.add_argument('-n', "--number", help="Number of messages to send.", type=int, default=1)
args = parser.parse_args()

syslog(message=args.message, level=args.level, host=args.host, port=args.port, number=args.number)
