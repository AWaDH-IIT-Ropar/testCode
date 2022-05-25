## gps.sh 

### Overview
* The script has only one iteration
* It configures the gps, enables it, takes a reading and disables the gps
* Runs only on boot, exits on acquiring gps signal
* The output is in json format at
> /tmp/gps

### Output
* The script outputs data in json

```
{
        "time":"2022-05-18T12:19:33",
        "gps_state":"gps_disabled",
        "location":{
                "status":"OK",
                "latitude":"3058.1217N",
                "longitude":"07628.4258E",
                "altitude":"255.0",
                "satellites":"05"
        }
}
```
