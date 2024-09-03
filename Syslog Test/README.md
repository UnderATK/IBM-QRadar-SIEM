# QRadar Service Checker

🚀 Boost Your Syslog Testing with This Script! 🛠️

As part of my work with IBM QRadar, I've developed a versatile script for testing SYSLOG—a critical component in cybersecurity for logging and monitoring. While it’s designed with QRadar in mind, this script is adaptable and can be used across various platforms that rely on SYSLOG for real-time log data.

🔍 What does it do?
  * Simulates different log sources and events.
  * Generates logs in standard SYSLOG formats.
  * Validates the integration of SYSLOG with your SIEM solution.

🔧 Why use it?
  * Streamline your testing process.
  * Ensure robust log monitoring.
  * Easily customize for different environments.

🔧 Features
  * Generate log as JSON format.

Whether you're setting up a new system, fine-tuning your existing security infrastructure, or just want to have a reliable tool in your cybersecurity toolkit, this script could be a game-changer.

### Installation:
```
  cd /
  mkdir scripts
  cd /scripts
  mkdir SyslogTest
  cd SyslogTest
  wget https://github.com/UnderATK/IBM-QRadar-SIEM/blob/main/Syslog%20Test/syslog_test.py
```

### Usage:
```
  python3 syslog_test.py [-h] [-m MESSAGE] [-l LEVEL] [-H HOST] [-p PORT] [-n NUMBER] [-j] [--version]

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
  -j, --json            Use JSON log format.
  --version             show program's version number and exit
```

### Examples:
* Regular:
  ```
  <6> 2024-09-03 14:35:26 HOSTNAME source_ip=192.168.0.1 destination_ip=127.0.0.1 msg=syslog test message
  ```
* JSON format:
  ```
  {'log_level': '6', 'timestamp': '2024-09-03 14:31:42', 'hostname': 'HOSTNAME', 'source_ip': '192.168.0.1', 'destination_ip': '127.0.0.1', 'msg': 'syslog test message'}
  ```
