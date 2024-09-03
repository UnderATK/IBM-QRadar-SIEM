# Cisco Talos IP Blacklist Importer
## **Supported QRadar API versions: <16.0**

### Installation:
1. create 'scripts' folder in your QRadar Console host.
   ```
   cd /
   mkdir scripts
   ```
2. move 'talosBlacklist.py' to 'scripts' folder using WinSCP or other tool.
3. move to scripts folder:
   ```
   cd /scripts/
   ```
4. download the script manually or using wget:
   ```
   wget https://github.com/UnderATK/IBM-QRadar-SIEM/blob/main/Cisco%20Talos%20IP%20Blacklist%20Importer/talosBlacklist.py
   ```
5. edit the script by adding your 'Authorized token you created in your QRadar:
   ```
   # Token
   token = ""
   ```
   add your QRadar URL to 'qradarUrl' variable:
   ```
   # URL
   qradarUrl = ""
   ```
6. Create Reference set in your QRadar environment named 'Talos IP Blacklist' with 'IP' values.
7. (Optional) Add the script to crontab to run automatically every 1H:
   ```
   crontab -e

   add this to the end of the file:
     0 * * * * /scripts/talosBlacklist.py > /dev/null 2>&1
   ```
8. run the script manually:
   ```
   python3 talosBlacklist.py
   ```
   
### Usage:
```
  python3 talosBlacklist.py [-h] [--version]

  options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
```

