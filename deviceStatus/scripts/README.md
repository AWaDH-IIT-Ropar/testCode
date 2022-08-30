## devdetect-bash.sh (Device Detection)

### Overview
* The status of detection and stored in json format in a file
> /tmp/devdetect

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
        "note":"1"
    },
    "camera":{
        "detect":"true",
        "model":"usb",
        "verify":"true",
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
  3. note: some description if any error occurred, in case of MMC, gives the current space used in percentage
  4. model: "usb", "csi"
  5. state: modem state
  6. failed_reason: modem failed reason
  7. signal: modem signal in percentage eg. "30 %"

## systemstats-ram.bash (System stats to RAM)

### Overview
* This script outputs a json object every 10s to 
> /tmp/devicestats

### Ouput
The script outputs data in json as
```
{
        "time":"2022-05-20T11:10:02",
        "cpuInfo":{
            "temperatures":{
                "A53":57.70,
                "A72":58.10
            },
            "usage":9.249,
            "usageDetailed":{
                "A53-0":16.290,
                "A53-1":10.029,
                "A53-2":16.290,
                "A53-3":7.178,
                "A72-0":2.956,
                "A72-1":2.846
            }
        },
        "gpuInfo":{
            "cores":2,
            "temperatures":{
                "GPU0":58.10,
                "GPU1":57.70
            },
            "memoryUsage":0.008
        },
        "ramInfo":{
            "total":3.626,
            "usage":19.167,
            "free":2.939
        },
        "generalInfo":{
            "board_serial":"06981200"
        },
        "internet":{
            "connectivity":true,
            "signal":0
        },
        "dataInfo":{
            "ethernet":{
                "rx":1958.245,
                "tx":558.313
            },
            "wwan":{
                "rx":0.000,
                "tx":0.000
            }
        },
        "powerInfo":{
            "battery_temp":-1,
            "voltage":-1,
            "avg_current":-1,
            "current":-1
        },
        "weather":{
            "lux":188.58,
            "temperature":24.99 ,
            "humidity":56.66 
        }
    }
```

## systemstats-sd.bash (System stats to SD card)

### Overview
* This script outputs in csv format every 60s to 
> /tmp/devicestats.csv

