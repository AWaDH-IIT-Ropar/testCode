#!/bin/bash

RED=0
GREEN=1
BLUE=2

FILE=/var/tmp/somefile

function get_val () {
    VAL=$(cat $FILE | python3 -c "import sys, json; print(json.load(sys.stdin)$1)")
}

function blink () {
    local REP=$1        # how many repetitions
    local COLOR=$2      # which color

    if [ "$COLOR" == "RED" ]; then
        COLOR_VAL=0
    elif [ "$COLOR" == "GREEN" ]; then
        COLOR_VAL=1
    elif [ "$COLOR" == "BLUE" ]; then
        COLOR_VAL=2
    fi

    for ((i = 1; i <= $REP; i++)); do
        if [ "$COLOR" == "YELLOW" ]; then
            # create yellow color
            echo 1 > /sys/class/pwm/pwmchip$RED/pwm0/enable
            echo 1 > /sys/class/pwm/pwmchip$GREEN/pwm0/enable
            sleep 0.5

            echo 0 > /sys/class/pwm/pwmchip$RED/pwm0/enable
            echo 0 > /sys/class/pwm/pwmchip$GREEN/pwm0/enable
            sleep 0.5
        else
            echo 1 > /sys/class/pwm/pwmchip$COLOR_VAL/pwm0/enable
            sleep 0.5
            echo 0 > /sys/class/pwm/pwmchip$COLOR_VAL/pwm0/enable
            sleep 0.5
        fi 
    done
}

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

    if [ -f "$FILE" ]; then
        # hts221 detect and verify
        get_val "['hts221']['detect']"
        HTS221_D=$VAL
        get_val "['hts221']['verify']"
        HTS221_V=$VAL

        # veml7700 detect and verify
        get_val "['veml7700']['detect']"
        VEML7700_D=$VAL
        get_val "['veml7700']['verify']"
        VEML7700_V=$VAL

        # modem detect and verify
        get_val "['modem']['detect']"
        MODEM_D=$VAL
        get_val "['modem']['verify']"
        MODEM_V=$VAL

        # camera detect and verify
        get_val "['camera']['detect']"
        CAM_D=$VAL
        get_val "['camera']['verify']"
        CAM_V=$VAL

        # mmc detect and verify
        get_val "['mmc']['detect']"
        MMC_D=$VAL
        get_val "['mmc']['verify']"
        MMC_V=$VAL


        # battery guage ic detect and verify
        get_val "['battery_ic']['detect']"
        BATT_GUAGE_D=$VAL
        get_val "['battery_ic']['verify']"
        BATT_GUAGE_V=$VAL
        

        if [ "$HTS221_D" == "false" ]; then
            blink "2" "RED"
            blink "3" "GREEN"
        else
            if [ "$HTS221_V" == "false" ]; then
                blink "2" "YELLOW"
                blink "3" "GREEN"
            fi
        fi

        if [ "$VEML7700_D" == "false" ]; then
            blink "2" "RED"
            blink "2" "GREEN"
            blink "1" "BLUE"
        else
            if [ "$VEML7700_V" == "false" ]; then
                blink "2" "YELLOW"
                blink "2" "GREEN"
                blink "1" "BLUE"
            fi
        fi

        if [ "$MODEM_D" == "false" ]; then
            blink "2" "RED"
            blink "1" "BLUE"
            blink "2" "GREEN"
        else
            if [ "$MODEM_V" == "false" ]; then
                blink "2" "YELLOW"
                blink "1" "BLUE"
                blink "2" "GREEN"
            fi
        fi

        if [ "$CAM_D" == "false" ]; then
            blink "2" "RED"
            blink "3" "BLUE"
        else
            if [ "$CAM_V" == "false" ]; then
                blink "2" "YELLOW"
                blink "3" "BLUE"
            fi
        fi

        if [ "$MMC_D" == "false" ]; then
            blink "2" "RED"
            blink "2" "BLUE"
            blink "1" "GREEN"
        else
            if [ "$MMC_V" == "false" ]; then
                blink "2" "YELLOW"
                blink "2" "BLUE"
                blink "1" "GREEN"
            fi
        fi

        if [ "$BATT_GUAGE_D" == "false" ]; then
            blink "2" "RED"
            blink "1" "GREEN"
            blink "2" "BLUE"
        else
            if [ "$BATT_GUAGE_V" == "false" ]; then
                blink "2" "YELLOW"
                blink "1" "GREEN"
                blink "2" "BLUE"
            fi
        fi
        
        echo "sleeping"
        sleep 5
    else
        echo "file not found"
    fi
done
