import json
from operator import mod
import time
from datetime import datetime
import logging
import deviceInfo

deviceInfo = deviceInfo.DeviceInfo()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')

file_handler = logging.FileHandler('/home/root/ws/devicestats.log', mode='a')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def compareTime(curHour,curMinute,ON_HOUR,ON_MINUTES,OFF_HOUR,OFF_MINUTES):
    if (ON_HOUR<curHour and curHour<OFF_HOUR):
        return True

    if ((ON_HOUR<curHour) or (ON_HOUR==curHour and ON_MINUTES<=curMinute)):
        if((curHour<OFF_HOUR) or (curHour==OFF_HOUR and curMinute<OFF_MINUTES)):
            return True
            
    return False

while True:

    try:
        with open(f'/etc/entomologist/ento.conf', 'r') as file:
            data = json.load(file)
    except:
        # logger.error("CONFIG FILE not found. Data not read")
        print("err")    

    ON_H, ON_M = map(int, data['device']['ON_TIME'].split(":"))
    OFF_H, OFF_M = map(int, data['device']['OFF_TIME'].split(":"))

    chour = datetime.now().hour
    cmin = datetime.now().minute
    csec = datetime.now().second
    
    if compareTime(chour, cmin, ON_H, ON_M, OFF_H, OFF_M):

        # logs data as A53-TEMP, A72-TEMP, CPU Usage
        # logger.info(f"{deviceInfo.getTemperatureCPUA53()}, {deviceInfo.getTemperatureCPUA72()}, {deviceInfo.getCPUUsage()}, {deviceInfo.getRAMUsage()}")

        tempA53 = deviceInfo.getTemperatureCPUA53()
        tempA72 = deviceInfo.getTemperatureCPUA72()
        tempGpu0 = deviceInfo.getTemperatureGPU0()
        tempGpu1 = deviceInfo.getTemperatureGPU1()
        cpu = deviceInfo.getCPUUsage()
        ram = deviceInfo.getRAMUsage()
        gpu = deviceInfo.getGPUMemoryUsage()
        
        logger.info(f"A53= {tempA53}, A72= {tempA72}, GPU0= {tempGpu0}, GPU1= {tempGpu1}, cpuUsage= {cpu}, ramUsage= {ram}, gpuUsage= {gpu}")

        # with open(f'/home/root/ws/devicestats.txt', 'a') as file:
        #     file.write(f"{chour}, {cmin}, {tempA53}, {tempA72}, {cpu}, {ram}\n")

        with open(f'/tmp/devicestats.txt', 'w') as file:
            # file.write(f"{deviceInfo.getTemperatureCPUA53()}, {deviceInfo.getTemperatureCPUA72()}, {deviceInfo.getCPUUsage()}, {deviceInfo.getRAMUsage()}")
            file.write(f"A53= {tempA53}, A72= {tempA72}, GPU0= {tempGpu0}, GPU1= {tempGpu1}, cpuUsage= {cpu}, ramUsage= {ram}, gpuUsage= {gpu}")
        time.sleep(10)
    else:
        time.sleep(10)
