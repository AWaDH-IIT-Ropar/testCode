#!/bin/bash

echo 353 > /sys/class/gpio/unexport
echo 353 > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio353/direction
echo 0 > /sys/class/gpio/gpio353/value

LEDSTATE=OFF

while true; do
    NETWORKSTATUS=$(nmcli -t -f STATE g)
    INTERNETSTATUS=$(ping -q -c 1 -W 1 8.8.8.8 | awk '/received/ {print $4}')

    if [ $NETWORKSTATUS = connected ]; then
        if [ $INTERNETSTATUS = 1 ]; then
            if [ $LEDSTATE = OFF ]; then
                LEDSTATE=ON
                echo 1 > /sys/class/gpio/gpio353/value
                echo "1" > /var/tmp/NETWORK
            fi
        else 
            echo 0 > /sys/class/gpio/gpio353/value
            echo "0" > /var/tmp/NETWORK
            if [ $LEDSTATE = OFF ]; then
                LEDSTATE=ON
                echo 1 > /sys/class/gpio/gpio353/value
                sleep 1
            else
                LEDSTATE=OFF
                echo 0 > /sys/class/gpio/gpio353/value
                sleep 1    
	        fi
        fi
    else
        echo 0 > /sys/class/gpio/gpio353/value
        echo "2" > /var/tmp/NETWORK
        LEDSTATE=OFF
    fi
done
