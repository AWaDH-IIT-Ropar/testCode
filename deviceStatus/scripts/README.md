## devdetect-bash.sh (Device Detection)

### Overview
* This scripts outputs either a _'0'_ (on detection success) or _'1'_ (on detection failure). In case of camera, either _'usb'_ or _'csi'_ will be written to file, depending on the camera attached.
* These values are stored in a file 
> /var/tmp/device-name
  
where device-name are:
  1. 'VEML7700', i2c sensor
  2. 'HTS221', i2c sensor
  3. 'CAM', camera.
  4. 'MMC', memorycard
  5. 'MODEM', 4G modem
  
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
