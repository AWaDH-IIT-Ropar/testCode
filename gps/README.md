## gps.sh 

### Overview
* The script has only one iteration
* It configures the gps, enables it, takes a reading and disables the gps
* Runs only on boot, exits on acquiring gps signal
* The output is in json format at
> /tmp/gps
  
### Execution
* Save the file in the required directory
* Give permission to execute with 
```
$ chmod 777 gps.sh
```
* Execute as
```
$ ./gps.sh
```

### Output
* The script outputs data in json
```
{
    "time":"2022-05-18T12:19:33",
    "gps_state":"gps_disabled",
    "config_info":{
        "config":"OK",
        "config_note":"configured"
    },
    "open_info":{
        "enable":"504",
        "enable_note":""
    },
    "close_info":{
        "disable":"OK",
        "disable_note":""
    },
    "location":{
        "status":"OK",
        "latitude":"3058.1217N",
        "longitude":"07628.4258E",
        "altitude":"255.0",
        "satellites":"05"
    }
}

```