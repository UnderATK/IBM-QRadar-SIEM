# Cisco Talos IP Blacklist Importer
### Installation:
1. create 'scripts' folder in your QRadar Console host.
```
  cd /
  mkdir scripts
```
2. move 'talosBlacklist.py' to 'scripts' folder.
3. edit the script by adding your 'Authorized token you created in your QRadar:
   ```
   # Token
    token = ""
   ```
  add your QRadar URL to 'qradarUrl' variable:
  ```
    # URL
    qradarUrl = ""
   ```
4. Create Reference set in your QRadar environment named 'Talos IP Blacklist' with 'IP' values.
   
### Usage:
```
  python3 talosBlacklist.py [-h] [--version]

  options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
```

