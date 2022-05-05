#!/bin/bash

RED=0
GREEN=1
BLUE=2

# Setup pwm pins
for I in {0..2}; do
    # Making sure the pwm chips aren't used
#    echo 0 > /sys/class/pwm/pwmchip$I/unexport
    
    # Start using the pins
    echo 0 > /sys/class/pwm/pwmchip$I/export
    
    # Setup period of PWM pins
    echo 1000000 > /sys/class/pwm/pwmchip$I/pwm0/period
    
    # Setup duty cycle of PWM pins
    echo 1000000 > /sys/class/pwm/pwmchip$I/pwm0/duty_cycle
done

sleep 1

while true; do
    HTS221=$(cat /var/tmp/HTS221 | head -1)
    VEML7700=$(cat /var/tmp/VEML7700 | head -1)
    MODEM=$(cat /var/tmp/MODEM | head -1)
    CAM=$(cat /var/tmp/CAM | head -1)
    MMC=$(cat /var/tmp/MMC | head -1)

	echo modem:$MODEM cam:$CAM mmc:$MMC veml:$VEML7700 hts:$HTS221
    if [[ $MODEM -ne 0 || $CAM -ne 0 || $MMC -ne 0 ]]; then
        # turn off green, blue
        echo 0 > /sys/class/pwm/pwmchip$GREEN/pwm0/enable
        echo 0 > /sys/class/pwm/pwmchip$BLUE/pwm0/enable

        # turn on red
        echo 1 > /sys/class/pwm/pwmchip$RED/pwm0/enable
    elif [[ $HTS221 -ne 0 || $VEML7700 -ne 0 ]];then
        # turn off green, red
        echo 0 > /sys/class/pwm/pwmchip$GREEN/pwm0/enable
        echo 0 > /sys/class/pwm/pwmchip$RED/pwm0/enable

        # turn on blue
        echo 1 > /sys/class/pwm/pwmchip$BLUE/pwm0/enable
    else
        # turn off red, blue
        echo 0 > /sys/class/pwm/pwmchip$RED/pwm0/enable
        echo 0 > /sys/class/pwm/pwmchip$BLUE/pwm0/enable

        # turn on green
        echo 1 > /sys/class/pwm/pwmchip$GREEN/pwm0/enable
    fi
    sleep 1
done
