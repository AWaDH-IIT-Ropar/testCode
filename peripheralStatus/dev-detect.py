#!/usr/bin/python3
import subprocess
import time
import smbus2
import serial
import sys
import json

def find_hts221():
    # Write data to address x5F(95), and register x20(32)
    data = 133 #0x85
    bus.write_byte_data(95, 32, data)
    bus.read_byte(95)

    # Read data from address x5F(95), and register x0F(15)
    data = bus.read_byte_data(95, 15)
    if(data == 188):
        sys.stdout.write("HTS221 FOUND\n")
        return "ok"
    else:
        sys.stderr.write("HTS221 NOT FOUND\n")
        return "err"

def find_veml7700():
    # https://github.com/muhammadrefa/python-i2c-scanner/blob/master/i2c-scanner.py
    # Read a byte from addres x10(16)
    if(bus.read_byte(16) == 0):
        sys.stdout.write("VEML7700 FOUND\n")
        return "ok"
    else:
        sys.stderr.write("VEML7700 NOT FOUND\n")
        return "err"

def find_mmc():
    # err = os.system("dmesg | grep 'mmc121: new' > /dev/null")
    out = subprocess.run("dmesg | grep 'mmc1: new' > /dev/null", shell=True)
    returncode = out.returncode
    if returncode:
        sys.stderr.write("MMC NOT FOUND\n")
        return "err"
    else:
        sys.stdout.write("MMC FOUND\n")
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
        sys.stdout.write("See3CAM_130 FOUND\n")
        return "ok"   
    if cam_model == "mxc-mipi-csi2.1":
        sys.stdout.write("Mipi Csi FOUND\n")
        return "ok"
    else:
        sys.stderr.write("CAM NOT FOUND\n")
        return "err"

def find_modem():
    modem = serial.Serial()
    modem.port = "/dev/ttyUSB2"
    modem.baudrate = 115200
    
    try:
        modem.open()
    except:
        res = "err"
        sys.stderr.write("Cannot open modem")

    if modem.isOpen():
        for i in range(0, 5):
            response = modem.read(modem.write(b"AT\r")+3)
            # modem.readlines()
            if(response == b"\r\nOK\r\n"):
                sys.stdout.write("MODEM FOUND\n")
                res = "ok"
                break
            else:
                # sys.stderr.write("MODEM NOT FOUND\n")
                res = "err"
            time.sleep(2)
        modem.close()

    if res == "err":
        sys.stderr.write("MODEM NOT FOUND\n")
        
    return res

if __name__ == "__main__":
    
    bus = smbus2.SMBus('/dev/apalis-i2c1')

    # Read file data
    try:
        with open(f"/home/root/ws/config.conf", 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        sys.stderr.write("File not found")
    
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
    except FileNotFoundError:
        sys.stderr.write("File not found")

