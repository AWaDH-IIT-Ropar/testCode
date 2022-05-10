## devdetect-bash.sh (Device Detection)

### Overview
* The status of detection and stored in json format in a file
> /var/tmp/somefile
  
### Execution
* Save the file in the required directory
* Give permission to execute with 
```
$ chmod 777 devdetect-bash.sh
```
* Execute as
```
$ ./devdetect-bash.sh
```

### Output
* The script outputs datat in json
```
{
    "veml7700":{
        "detect":"true",
        "verify":"true",
        "note":""
    },
    "hts221":{
        "detect":"true",
        "verify":{
            "temp":"true",
            "humidity":"true"
        },
        "note":""
    },
    "battery_ic":{
        "detect":"true",
        "verify":"true",
        "note":""
    },
    "mmc":{
        "detect":"true",
        "verify":"true",
        "note":""
    },
    "camera":{
        "detect":"true",
        "model":"usb",
        "verify":"",
        "note":""
    },
    "modem":{
        "detect":"false",
        "verify":"false",
        "state":"",
        "failedreason":"",
        "signal":"",
        "note":"cmd_err"
    }
}
```
* The possible values for keys are
  1. detect: "true", "false"
  2. verify: "true", "false". NOTE hts221 has temp and humidity keys in verify
  3. note: some description if any error occurred
  4. model: "usb", "csi"
  5. state: modem state
  6. failed_reason: modem failed reason
  7. signal: modem signal in percentage eg. "30 %"

## systemstats.py (System stats)

### Overview
* This script outputs a json object every 10s to 
> /var/tmp/deviceStatus.conf
* The outputs are
  1. time in ISO format
  2. cpu information
  3. gpu information
  4. ram information
  5. general board information
  6. internet connectivity
  
### Requirements
  1. psutil (python module)
  2. deviceinfo.py (present in the same directory of repo)
  
### Execution
* Save the file in the required directory
* Execute as
```
$ python3 /the/directory/of/file/systemstats.py
```
