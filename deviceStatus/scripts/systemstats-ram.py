import time
import urllib.request
import deviceInfo
from datetime import datetime as date
import subprocess
from os.path import exists
import csv
import json

deviceInfo = deviceInfo.DeviceInfo()

def cpu_info():
    ret = {
        'temperatures': {
            'A53': 0.0,
            'A72': 0.0
        },
        'usage': 0.0,
        'usageDetailed': {
            'A53-0': 0.0,
            'A53-1': 0.0,
            'A53-2': 0.0,
            'A53-3': 0.0,
            'A72-0': 0.0,
            'A72-1': 0.0
        }
    } 
    
    ret['temperatures'] = {
        'A53': deviceInfo.getTemperatureCPUA53(),
        'A72': deviceInfo.getTemperatureCPUA72()
    }
    
    ret['usage'] = deviceInfo.getCPUUsage()

    det = deviceInfo.getCPUUsageDetailed()
    
    ret['usageDetailed'] = {
        'A53-0': det[0],
        'A53-1': det[1],
        'A53-2': det[2],
        'A53-3': det[3],
        'A72-0': det[4],
        'A72-1': det[5],
    }

    return ret

def gpu_info():
    ret = {
        'cores': 2, 
        'temperatures': [],
        'memoryUsage': float("{:.3f}".format(deviceInfo.getGPUMemoryUsage()))
    }
    
    ret['temperatures'] = {
        'GPU0': deviceInfo.getTemperatureGPU0(),
        'GPU1': deviceInfo.getTemperatureGPU1()
    }

    return ret

def ram_info():
    ret = {
        'total': deviceInfo.getRAMTotal(), 
        'usage': deviceInfo.getRAMUsage(),
        'free': deviceInfo.getRAMFree()
    }

    return ret

def general_info():
    ret = {
        'board-serial': deviceInfo.getTdxSerialNumber(),
        'board-type': deviceInfo.getTdxProductID(),
        'board-revision': deviceInfo.getTdxProductRevision()
    }
    
    return ret

def internet_info():
    ret = {
        'connectivity': "False",
        'signal': 0
    }
    host = 'http://google.com'
    try:
        urllib.request.urlopen(host)
        connected = True
    except:
        connected = False

    if connected:
        ret['connectivity'] = "True"
    
    signal_str = subprocess.run("mmcli -m 0 | \
        awk '/signal quality/ {print $4}'", \
        shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.rstrip('%\n')

    ret['signal'] = signal_str
    return ret

def data_usage_info():
    ret = {
        "ethernet": {
            "rx": 0,
            "tx": 0
        },
        "wwan": {
            "rx": 0,
            "tx": 0
        }
    }
    data = subprocess.run("vnstat -i eth0 --json y", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.rstrip('\n')
    try:
        dataj = json.loads(data)
        ret['ethernet']['rx'] = float("{:.3f}".format(dataj["interfaces"][0]["traffic"]["total"]["rx"]/(1024*1024)))
        ret['ethernet']['tx'] = float("{:.3f}".format(dataj["interfaces"][0]["traffic"]["total"]["tx"]/(1024*1024)))
    except:
        ret['ethernet']['rx'] = -1
        ret['ethernet']['tx'] = -1

    data = subprocess.run("vnstat -i wwan0 --json y", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.rstrip('\n')

    try:
        dataj = json.loads(data)
        ret['wwan']['rx'] = float("{:.3f}".format(dataj["interfaces"][0]["traffic"]["total"]["rx"]/(1024*1024)))
        ret['wwan']['tx'] = float("{:.3f}".format(dataj["interfaces"][0]["traffic"]["total"]["tx"]/(1024*1024)))
    except:
        ret['wwan']['rx'] = -1
        ret['wwan']['tx'] = -1

    return ret

def power_info():
    ret = {
            "battery_temp": -1,
            "voltage": -1,
            "avg_current": -1,
            "current": -1
        }

    if(exists("/tmp/battery_parameters")):
        temp = subprocess.run("cat /tmp/battery_parameters | awk 'NR == 1 {print $3}'", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.rstrip('\n')
        if temp != "":
            temp = float(temp)
        else:
            temp = float(-1)

        voltage = subprocess.run("cat /tmp/battery_parameters | awk 'NR == 2 {print $3}'", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.rstrip('\n')
        if voltage != "":
            voltage = float(voltage)/1000
        else:
            voltage = float(-1)

        avg_current = subprocess.run("cat /tmp/battery_parameters | awk 'NR == 3 {print $4}'", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.rstrip('\n')
        if avg_current != "":
            avg_current = float(avg_current)/1000
        else:
            avg_current = float(-1)

        current = subprocess.run("cat /tmp/battery_parameters | awk 'NR == 4 {print $3}'", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.rstrip('\n')
        if current != "":
            current = float(current)/1000
        else:
            current = float(-1)

        ret['battery_temp'] = temp
        ret['voltage'] = voltage
        ret['avg_current'] = avg_current
        ret['current'] = current

        return ret
    else:
        return ret

def get_allinfo():
    getCpu = cpu_info()
    getGpu = gpu_info()
    getRam = ram_info()
    getGeneral = general_info()
    getInternet = internet_info()
    getData = data_usage_info()
    getPower = power_info()

    ret = {
        "time" : date.isoformat(date.now()),
        "cpuInfo": getCpu,
        "gpuInfo": getGpu,
        "ramInfo": getRam,
        "generalInfo": getGeneral,
        "internet": getInternet,
        "dataInfo": getData,
        "powerInfo": getPower
    }

    return ret

if __name__ == '__main__':

    while True:
        status = get_allinfo()
        # write to file every 10 seconds
        with open("/tmp/devicestats", 'w') as file:
            json.dump(status, file, indent=4, separators=(',', ':'))
        time.sleep(10)
            
