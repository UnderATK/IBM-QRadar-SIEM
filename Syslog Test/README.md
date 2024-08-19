# QRadar Service Checker
### Installation:
```
  mkdir SyslogTest
  cd SyslogTest
  wget https://github.com/UnderATK/IBM-QRadar-SIEM/blob/main/Syslog%20Test/syslog_test.py
```

### Usage:
```
  python3 syslog_test.py [-h] [-m MESSAGE] [-l LEVEL] [-H HOST] [-p PORT] [-n NUMBER] [--version]

  options:
  -h, --help            show this help message and exit
  -m MESSAGE, --message MESSAGE
                        Syslog message.
  -l LEVEL, --level LEVEL
                        Syslog level: emergency=0 alert=1 critical=2 error=3 warning=4 notice=5 info=6 debug=7
  -H HOST, --host HOST  Remote syslog server ip.
  -p PORT, --port PORT  Remote syslog server port.
  -n NUMBER, --number NUMBER
                        Number of messages to send.
  --version             show program's version number and exit
```
