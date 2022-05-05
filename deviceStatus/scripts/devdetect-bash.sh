#!/bin/bash

# 0 in the file means detected
# 1 in the file means not detected

########################## veml7700 ##########################
VEML7700=$(i2cdetect -y -r 4 | awk '/10/ {print $2}')

if [ $VEML7700 = 10 ]; then
        echo "0" > /var/tmp/VEML7700
else
    	echo "1" > /var/tmp/VEML7700
fi

VEML7700=$(/usr/sbin/weather/VEML7700 | awk '{print $4}')
if [ $(echo "$VEML7700>4000" | bc) = 1 ]; then
	echo "error" >> /var/tmp/VEML7700
elif [ $(echo "$VEML7700<0" | bc) = 1 ]; then
	echo "error" >> /var/tmp/VEML7700
else
    echo "verified" >> /var/tmp/VEML7700
fi
########################## veml7700 ##########################

########################## HTS221 ############################
HTS221=$(i2cdetect -y -r 4 | awk '/50/ {print $17}')

if [ $HTS221 = 5f ]; then
        echo "0" > /var/tmp/HTS221
else
    	echo "1" > /var/tmp/HTS221
fi

HTS221_TEMP=$(/usr/sbin/weather/hts221 | awk '/Celsius/ {print $5}')
HTS221_HUM=$(/usr/sbin/weather/hts221 | awk '/humidity/ {print $4}')

if [ $(echo "$HTS221_HUM>100" | bc) = 1 ]; then
	echo "humidity error" >> /var/tmp/HTS221
elif [ $(echo "$HTS221_HUM<0" | bc) = 1 ]; then
	echo "humidity error" >> /var/tmp/HTS221
else
    	echo "humidity verified" >> /var/tmp/HTS221
fi

if [ $(echo "$HTS221_TEMP>120" | bc) = 1 ]; then
	echo "temperature error" >> /var/tmp/HTS221
elif [ $(echo "$HTS221_TEMP<-40" | bc) = 1 ]; then
	echo "temperature error" >> /var/tmp/HTS221
else
    	echo "temperature verified" >> /var/tmp/HTS221
fi
########################## HTS221 ############################

########################## CAMERA ############################
CAM=$(cat /sys/class/video4linux/*/name | awk '/Video Capture 4/ || /mxc-mipi-csi2.1/ {print $1}')

if [ $CAM = "mxc-mipi-csi2.1" ]; then
	echo "csi" > /var/tmp/CAM
elif [ $CAM = "Video" ]; then
	echo "usb" > /var/tmp/CAM
else
	echo "1" > /var/tmp/CAM
fi
########################## CAMERA ############################

########################## MMC ###############################
MMC=$(cat /sys/kernel/debug/gpio | awk '/gpio-425/ {print $6}')

if [ $MMC = "lo" ]; then
    echo "0" > /var/tmp/MMC
else
    echo "1" > /var/tmp/MMC
fi
########################## MMC ###############################

########################## MODEM #############################
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

L1=$(mmcli -m 0 | awk '/Status/ {print NR}')
L2=`expr $(mmcli -m 0 | awk '/Modes/ {print NR}') - 2`

STATE=$(mmcli -m 0 | awk -v l1=$L1 -v l2=$L2 'NR == l1,NR == l2 {print $0}' | awk '/state/ {print $0}' | awk 'NR == 1 {print $NF}')
SIGNAL=$(mmcli -m 0 | awk '/signal/ {print $4}')

echo "state: $STATE" >> /var/tmp/MODEM
# if [ $STATE = "failed" ]; then
    echo "failed reason: $(mmcli -m 0 | awk '/failed reason/ {print $4}')" >> /var/tmp/MODEM
# fi
echo "signal: $SIGNAL" >> /var/tmp/MODEM
########################## MODEM #############################
