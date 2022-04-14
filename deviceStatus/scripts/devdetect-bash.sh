#!/bin/bash

# Find veml7700
VEML7700=$(i2cdetect -y -r 4 | awk '/10/ {print $2}')

if [ $VEML7700 = 10 ]; then
        echo "0" > /var/tmp/VEML7700
else
    	echo "1" > /var/tmp/VEML7700
fi

# Find hts221
HTS221=$(i2cdetect -y -r 4 | awk '/50/ {print $17}')

if [ $HTS221 = 5f ]; then
        echo "0" > /var/tmp/HTS221
else
    	echo "1" > /var/tmp/HTS221
fi

# Find camera
CAM=$(cat /sys/class/video4linux/*/name | awk '/Video Capture 4/ || /mxc-mipi-csi2.1/ {print $1}')

if [ $CAM = "mxc-mipi-csi2.1" ]; then
	echo "csi" > /var/tmp/CAM
elif [$CAM = "Video" ]; then
	echo "usb" > /var/tmp/CAM
else
	echo "1" > /var/tmp/CAM
fi

# Find memory card

# dmesg | grep 'mmc1: new' > /dev/null
# if [ $? = 0 ]; then
# 	echo "0" > /var/tmp/MMC
# else
# 	echo "1" > /var/tmp/MMC
# fi

# Detect MMC with hardware detection pin
MMC=$(cat /sys/kernel/debug/gpio | awk '/gpio-425/ {print $6}')

if [ $MMC = "lo" ]; then
    echo "0" > /var/tmp/MMC
else
    echo "1" > /var/tmp/MMC
fi

# Find modem
# MODEM=$(echo -ne "AT\r\n" | microcom -t 5 -X /dev/ttyUSB2 -s 115200 | grep "OK")

sleep 2
MODEM=$(echo -ne "AT\r\n" | microcom -t 100 -X /dev/ttyUSB2 -s 115200 | awk '/OK/ {print $1}')

# check if MODEM is  empty variable
COUNT=100
while [[ -z "$MODEM" && "$COUNT" -ne 0 ]]; do
    MODEM=$(echo -ne "AT\r\n" | microcom -t 100 -X /dev/ttyUSB2 -s 115200 | awk '/OK/ {print $1}')
done

if [ $MODEM = "OK" ]; then
	echo "0" > /var/tmp/MODEM
else
	echo "1" > /var/tmp/MODEM
fi