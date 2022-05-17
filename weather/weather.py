from datetime import datetime as date
from os.path import exists
import subprocess
import time
import json
import csv

def weather():
    lux = subprocess.run("cat /tmp/light_intensity | awk '{print $4}'", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.rstrip('\n')
    humidity = subprocess.run("cat /tmp/met | awk '/Relative Humidity/ {print $4}'", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.rstrip('\n')
    tempC = subprocess.run("cat /tmp/met | awk '/Temperature in C:/ {print $4}'", shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.rstrip('\n')

    timeH = date.today().strftime("%d-%m-%Y_%H")
    weatherFile = f"{STORAGE_PATH}weather_{timeH}_{DEVICE_SERIAL_ID}.csv"
    
    if(exists(weatherFile)):
        with open(weatherFile, mode='a') as csv_file:
            fieldnames = ['Date', 'Time', 'Lux', 'Humidity', 'TemperatureC']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({'Date': date.today().strftime("%d/%m/%y"), 'Time': date.now().strftime("%H:%M:%S"), 'Lux':lux, 'Humidity': humidity, 'TemperatureC': tempC})
    else:
        with open(weatherFile, mode='w') as csv_file:
            fieldnames = ['Date', 'Time', 'Lux', 'Humidity', 'TemperatureC']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'Date': date.today().strftime("%d/%m/%y"), 'Time': date.now().strftime("%H:%M:%S"), 'Lux':lux, 'Humidity': humidity, 'TemperatureC': tempC})

# Read device id, storage path
with open("/etc/entomologist/ento.conf",'r') as file:
    data = json.load(file)

DEVICE_SERIAL_ID = data["device"]["SERIAL_ID"]
STORAGE_PATH = data["device"]["STORAGE_PATH"]

while True:
    try:
        weather()
        time.sleep(30)
    except Exception as e:
        print(e)
        time.sleep(10)
