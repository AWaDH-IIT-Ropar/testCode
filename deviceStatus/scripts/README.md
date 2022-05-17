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
* The script outputs data in json
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
        "detect":"false",
        "verify":"false",
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
        "detect":"true",
        "verify":"false",
        "state":"failed",
        "failed_reason":"sim-missing",
        "signal":"0%",
        "note":""
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
> /var/tmp/devicestats
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

### Ouput
The script outputs data in json as
```
{
    "time":"2022-05-10T15:32:43.842498",
    "cpuInfo":{
        "temperatures":{
            "A53":50.3,
            "A72":51.3
        },
        "usage":2.8,
        "usageDetailed":{
            "A53-0":1.1,
            "A53-1":7.5,
            "A53-2":1.0,
            "A53-3":0.8,
            "A72-0":6.1,
            "A72-1":0.6
        }
    },
    "gpuInfo":{
        "cores":2,
        "temperatures":{
            "GPU0":51.3,
            "GPU1":51.3
        },
        "memoryUsage":0.007635354995727539
    },
    "ramInfo":{
        "total":3.626,
        "usage":16.5,
        "free":3.0146
    },
    "generalInfo":{
        "board-serial":6981200,
        "board-type":"0037",
        "board-revision":"V1.1C"
    },
    "internet":{
        "connectivity":"False",
        "signal":"0"
    },
    "dataInfo":{
        "rx":383.34935092926025,
        "tx":61.435561180114746
    },
    "powerInfo":{
        "battery_temp":25.55,
        "voltage":12.453,
        "avg_current":0.452,
        "current":0.004
    }
}
```
