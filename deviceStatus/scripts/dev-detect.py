#!/usr/bin/python3
import subprocess
import time
import smbus2
import serial
import sys
import json
import logging

# Logging stuff
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')

file_handler = logging.FileHandler('/var/tmp/devdetect.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def find_hts221():
    # Write data to address x5F(95), and register x20(32)
    data = 133 #0x85
    bus.write_byte_data(95, 32, data)
    bus.read_byte(95)

    # Read data from address x5F(95), and register x0F(15)
    data = bus.read_byte_data(95, 15)
    if(data == 188):
        logger.info("HTS221 found")
        return "ok"
    else:
        logger.error("HTS221 not found")
        return "err"

def find_veml7700():
    # Read a byte from addres x10(16)
    if(bus.read_byte(16) == 0):
        logger.info("VEML7700 found")
        return "ok"
    else:
        logger.error("VEML7700 not found")
        return "err"

def find_mmc():
    out = subprocess.run("dmesg | grep 'mmc1: new' > /dev/null", shell=True)
    returncode = out.returncode
    if returncode:
        logger.error("MMC not found")
        return "err"
    else:
        logger.info("MMC found")
        return "ok"

def find_camera():
    '''
    cam_model = subprocess.run("v4l2-ctl -d2 -D | awk '/Model/ {print $3}'", \
        shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.rstrip('\n')
    '''
    cam_model = subprocess.run("cat /sys/class/video4linux/*/name | \
        awk '/Video Capture 4/ || /mxc-mipi-csi2.1/ {print $1}'", \
        shell=True, stdout=subprocess.PIPE, universal_newlines=True).stdout.rstrip('\n')

    if cam_model == "Video":
        logger.info("See3CAM_130 found")
        return "ok"   
    if cam_model == "mxc-mipi-csi2.1":
        logger.info("MIPI CSI found")
        return "ok"
    else:
        logger.error("CAM not found")
        return "err"

def find_modem():
    modem = serial.Serial()
    modem.port = "/dev/ttyUSB2"
    modem.baudrate = 115200
    
    try:
        modem.open()
    except:
        res = "err"
        logger.error("Cannot open modem port")

    if modem.isOpen():
        for i in range(0, 5):
            response = modem.read(modem.write(b"AT\r")+3)
            if(response == b"\r\nOK\r\n"):
                logger.info("MODEM found")
                res = "ok"
                break
            else:
                res = "err"
            time.sleep(2)
        modem.close()

    if res == "err":
        logger.error("MODEM not found")
        
    return res

if __name__ == "__main__":
    
    bus = smbus2.SMBus('/dev/apalis-i2c1')

    # Read file data
    try:
        with open(f"/home/root/ws/config.conf", 'r') as file:
            data = json.load(file)
    except:
        logger.error("CONFIG FILE not found. Data not read")
    
    # Wait for modem to start its serial port
    time.sleep(10)

    # Get peripherals status
    hts221 = find_hts221()
    veml7700 = find_veml7700()
    mmc = find_mmc()
    cam = find_camera()
    modem = find_modem()
    
    # Write data to file
    try:
        with open(f"/home/root/ws/config.conf", 'w') as file:
            data["peripherals"].update({"HTS221": hts221})
            data["peripherals"].update({"VEML7700": veml7700})
            data["peripherals"].update({"MMC": mmc})
            data["peripherals"].update({"CAM": cam})
            data["peripherals"].update({"MODEM": modem})
            json.dump(data, file, indent=4, separators=(',', ':'))
    except:
        logger.error("CONFIG FILE not found. Data not written")
