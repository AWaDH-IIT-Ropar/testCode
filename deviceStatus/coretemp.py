import json
import time
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')

file_handler = logging.FileHandler('/var/tmp/devicetemp.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def compareTime(curHour,curMinute,ON_HOUR,ON_MINUTES,OFF_HOUR,OFF_MINUTES):
    if (ON_HOUR<curHour and curHour<OFF_HOUR):
        return True

    if ((ON_HOUR<curHour) or (ON_HOUR==curHour and ON_MINUTES<=curMinute)):
        if((curHour<OFF_HOUR) or (curHour==OFF_HOUR and curMinute<OFF_MINUTES)):
            return True
            
    return False

def gettemp(index):
    f = open("/sys/class/thermal/thermal_zone" + str(index) + "/temp")
    temp = int(f.read())
    return float(temp) / 1000.0

while True:

    try:
        with open(f'/etc/entomologist/ento.conf', 'r') as file:
            data = json.load(file)
    except:
        logger.error("CONFIG FILE not found. Data not read")
   
    ON_H, ON_M = map(int, data['device']['ON_TIME'].split(":"))
    OFF_H, OFF_M = map(int, data['device']['OFF_TIME'].split(":"))

    chour = datetime.now().hour
    cmin = datetime.now().minute
    csec = datetime.now().second
    
    if compareTime(chour, cmin, ON_H, ON_M, OFF_H, OFF_M):
        core1 = gettemp(0)
        core2 = gettemp(1)
        core3 = gettemp(2)
        core4 = gettemp(3)
        
        # logs data as A52-TEMP, A72-TEMP, GPU0-TEMP, GPU1-TEMP
        logger.info(f"{core1}, {core2}, {core3}, {core4}")

        with open(f'/tmp/temperaturelog.txt', 'w') as file:
            file.write(f"{chour}, {cmin}, {csec}, {core1}, {core2}, {core3}, {core4}\n")
        time.sleep(10)
    else:
        time.sleep(10)
