#!/bin/bash

# making sure some things are setup
vnstat -i wwan0 --add 
systemctl restart vnstat.service

systemctl mask wpa_supplicant.service

# variable names are in caps

function veml7700_detect () {
    local CHECK=$(i2cdetect -y -r 4 | awk '/10/ {print $2}')

    if [ $CHECK = 10 ]; then
        VEML7700_DETECT="true"
        printf "VEML7700 Detected\n"
    else
        VEML7700_DETECT="false"
        printf "VEML7700 Not Detected\n"
    fi
}

function veml7700_verify () {
    if [ -f "/usr/sbin/light/light_intensity" ]; then
        $(/usr/sbin/light/light_intensity test)
        local CHECK=$(cat /tmp/light_intensity | awk '{print $4}')
        if [ -z $CHECK ]; then
            VEML7700_NOTE="no_reading"
            VEML7700_VERIFY="false"
        elif [ $(echo "$CHECK>4000" | bc) = 1 ]; then
            VEML7700_NOTE="value_err_hi"
            VEML7700_VERIFY="false"
        elif [ $(echo "$CHECK<0" | bc) = 1 ]; then
            VEML7700_NOTE="value_err_lo"
            VEML7700_VERIFY="false"
        else
            VEML7700_VERIFY="true"
        fi

        if [ $VEML7700_VERIFY == "true" ]; then
            printf "VEML7700 Verified\n"
        else
            printf "VEML7700 Not Verified\n"
        fi
    else
        VEML7700_NOTE="binary_file_err"
        VEML7700_VERIFY="false"
        printf "VEML7700 Not Verified\n"
    fi
}

function hts221_detect () {
    local CHECK=$(i2cdetect -y -r 4 | awk '/50/ {print $17}')

    if [ $CHECK = 5f ]; then
        HTS221_DETECT="true"
        printf "HTS221 Detected\n"
    else
        HTS221_DETECT="false"
        printf "HTS221 Not Detected\n"
    fi
}

function hts221_verify () {
    
    if [ -f "/usr/sbin/met/TH_reading" ]; then
        $(/usr/sbin/met/TH_reading test)
        local CHECK_TEMP=$(cat /tmp/met | awk '/Temperature in C/ {print $4}')
        local CHECK_HUM=$(cat /tmp/met | awk '/Relative Humidity/ {print $4}')

        if [ -z "$CHECK_HUM" ]; then
            HTS221_NOTE="no_reading"
            HTS221_VERIFY_HUM="false"
        elif [ $(echo "$CHECK_HUM>100" | bc) = 1 ]; then
            HTS221_NOTE="value_err_hi"
            HTS221_VERIFY_HUM="false"
        elif [ $(echo "$CHECK_HUM<0" | bc) = 1 ]; then
            HTS221_NOTE="value_err_lo"
            HTS221_VERIFY_HUM="false" 
        else
            HTS221_VERIFY_HUM="true"
        fi

        if [ $HTS221_VERIFY_HUM == "true" ]; then
            printf "HTS221 Humidity Verified\n"    
        else
            printf "HTS221 Humidity Not Verified\n"
        fi

        if [ -z "$CHECK_TEMP" ]; then
            $(/usr/sbin/weather/hts221)
            HTS221_NOTE="no_reading"
            HTS221_VERIFY_TEMP="false"
        elif [ $(echo "$CHECK_TEMP>120" | bc) = 1 ]; then
            HTS221_NOTE="value_err_hi"
            HTS221_VERIFY_TEMP="false"
        elif [ $(echo "$CHECK_TEMP<-40" | bc) = 1 ]; then
            HTS221_NOTE="value_err_lo"
            HTS221_VERIFY_TEMP="false"
        else
            HTS221_VERIFY_TEMP="true"
        fi

        if [ $HTS221_VERIFY_TEMP == "true" ]; then
            printf "HTS221 Temperature Verified\n"
        else
            printf "HTS221 Temperature Not Verified\n"
        fi
    else
        HTS221_NOTE="binary_file_err"
        HTS221_VERIFY_HUM="false"
        HTS221_VERIFY_TEMP="false"
        printf "HTS221 Not Verified"
    fi
}

function camera_detect () {
    local CHECK=$(cat /sys/class/video4linux/*/name | awk '/Video Capture 4/ || /mxc-mipi-csi2.1/ {print $1}')

    if [[ -z "$CHECK" ]]; then
        CAM_DETECT="false"
        printf "Camera Not Detected\n"
    else
        CAM_DETECT="true"
        if [ $CHECK = "mxc-mipi-csi2.1" ]; then
            CAM_MODEL="csi"
            printf "MIPI CSI Camera Detected\n"
        elif [ $CHECK = "Video" ]; then
            CAM_MODEL="usb"
            printf "SeeCAM31 camera Detected\n"
        fi
    fi
}

function camera_verify () {
    printf "Camera Verify Not Implemented\n"
    CAM_VERIFY="true"
}

function mmc_detect () {
    local CHECK=$(cat /sys/kernel/debug/gpio | awk '/gpio-425/ {print $6}')

    if [ $CHECK = "lo" ]; then
        MMC_DETECT="true"
        printf "MMC Detected\n"
    else
        MMC_DETECT="false"
        printf "MMC Not Detected\n"
    fi
}

function mmc_verify () {
    local RAND_W=$(cat /proc/sys/kernel/random/uuid)
    echo $RAND_W > /media/mmcblk1p1/random

    local RAND_R=$(cat /media/mmcblk1p1/random)

    if [[ $RAND_W = $RAND_R ]]; then
        MMC_VERIFY="true"
        printf "MMC Verified\n"
    else
        MMC_VERIFY="false"
        printf "MMC Not Verified\n"
    fi

    rm -f /media/mmcblk1p1/random > /dev/null 2>&1
    mkdir /media/mmcblk1p1/upload > /dev/null 2>&1
}

function modem_detect () {
    local CHECK=$(echo -ne "AT\r\n" | microcom -t 100 -X /dev/ttyUSB2 -s 115200 | awk '/OK/ {print $1}')
    
    if [ -z "$CHECK" ]; then
        MODEM_DETECT="false"
        MODEM_NOTE="cmd_err"
        printf "Modem Not Detected\n"
    elif [ $CHECK = "OK" ]; then
        MODEM_DETECT="true"
        printf "Modem Detected\n"
    fi
}

function modem_verify () {
    mmcli -m 0 > /dev/null 2>&1
    if [ "echo $?" = 1 ]; then
        MODEM_NOTE="cmd_err"
        MODEM_VERIFY="false"
        printf "Modem Not Verified\n"
    fi

    if [ "$MODEM_NOTE" != "cmd_err" ]; then

        L1=$(mmcli -m 0 | awk '/Status/ {print NR}')
        L2=`expr $(mmcli -m 0 | awk '/Modes/ {print NR}') - 2`

        MODEM_STATE=$(mmcli -m 0 | awk -v l1=$L1 -v l2=$L2 'NR == l1,NR == l2 {print $0}' | awk '/state/ {print $0}' | awk 'NR == 1 {print $NF}' | perl -pe 's/\e\[[\x30-\x3f]*[\x20-\x2f]*[\x40-\x7e]//g;s/\e[PX^_].*?\e\\//g;s/\e\][^\a]*(?:\a|\e\\)//g;s/\e[\[\]A-Z\\^_@]//g;')

        #if modem disabled, enable it
        if [[ "$MODEM_DETECT" == "true" && "$MODEM_STATE" == "disabled" ]]; then
            mmcli -m 0 -e > /dev/null 2>&1
        fi

        MODEM_STATE=$(mmcli -m 0 | awk -v l1=$L1 -v l2=$L2 'NR == l1,NR == l2 {print $0}' | awk '/state/ {print $0}' | awk 'NR == 1 {print $NF}' | perl -pe 's/\e\[[\x30-\x3f]*[\x20-\x2f]*[\x40-\x7e]//g;s/\e[PX^_].*?\e\\//g;s/\e\][^\a]*(?:\a|\e\\)//g;s/\e[\[\]A-Z\\^_@]//g;')
        MODEM_SIGNAL=$(mmcli -m 0 | awk '/signal/ {print $4}')
        MODEM_FAILED_REASON=$(mmcli -m 0 | awk '/failed reason/ {print $4}' | perl -pe 's/\e\[[\x30-\x3f]*[\x20-\x2f]*[\x40-\x7e]//g;s/\e[PX^_].*?\e\\//g;s/\e\][^\a]*(?:\a|\e\\)//g;s/\e[\[\]A-Z\\^_@]//g;')

        if [[ "$MODEM_STATE" == "failed" ]]; then
            MODEM_VERIFY="false"
            printf "Modem Not Verified\n"
        else
            MODEM_VERIFY="true"
            printf "Modem Verified\n"
        fi
    fi

    # if [ "$MODEM_STATE" == "failed" ]; then
    #     MODEM_VERIFY="false"
    # fi
}

function battery_guage_detect () {
    local CHECK=$(i2cdetect -y -r 4 | awk '/50/ {print $7}')

    if [ $CHECK = 55 ]; then
        BATT_GUAGE_DETECT="true"
        printf "Battery Guage Detected\n"
    else
        BATT_GUAGE_DETECT="false"
        printf "Battery Guage Not Detected\n"
    fi
}

function battery_guage_verify () {
    i2cset -y 4 0x55 0x00 0x0001 w
    local CHECK=$(i2cget -y 4 0x55 0x00 w | awk '{print $0}')

    if [ -z "$CHECK" ]; then
        BATT_GUAGE_VERIFY="false"
        BATT_GUAGE_NOTE="cmd_err"
        printf "Battery Guage Not Verified\n"
    fi
    if [ $CHECK = 0x0100 ]; then
        BATT_GUAGE_VERIFY="true"
        printf "Battery Guage Verified\n"
    fi
}

while true; do 
    dmesg | grep "pcie_switch: disabling"
    if [ $? = 0 ]; then
        break
    fi
    sleep 1
done

# veml7700
veml7700_detect
if [ "$VEML7700_DETECT" == "true" ]; then
    veml7700_verify
else
    VEML7700_VERIFY="false"
fi

# hts221
hts221_detect
if [ "$HTS221_DETECT" == "true" ]; then
    hts221_verify
else
    HTS221_VERIFY_HUM="false"
    HTS221_VERIFY_TEMP="false"
fi

# camera
camera_detect
if [ "$CAM_DETECT" == "true" ]; then
    camera_verify
else
    CAM_VERIFY="false"
fi

# mmc
mmc_detect
if [ "$MMC_DETECT" == "true" ]; then
    mmc_verify
else
    MMC_VERIFY="false"
fi

modem_detect
if [ "$MODEM_DETECT" == "true" ]; then
    modem_verify
else
    MODEM_VERIFY="false"
fi

# battery guage ic
battery_guage_detect
if [ "$BATT_GUAGE_DETECT" == "true" ]; then
    battery_guage_verify
else
    BATT_GUAGE_VERIFY="false"
fi


echo "{\"veml7700\":{\"detect\":\"$VEML7700_DETECT\",\"verify\":\"$VEML7700_VERIFY\",\"note\":\"$VEML7700_NOTE\"},\"hts221\":{\"detect\":\"$HTS221_DETECT\",\"verify\":{\"temp\":\"$HTS221_VERIFY_TEMP\",\"humidity\":\"$HTS221_VERIFY_HUM\"},\"note\":\"$HTS221_NOTE\"},\"battery_ic\":{\"detect\":\"$BATT_GUAGE_DETECT\",\"verify\":\"$BATT_GUAGE_VERIFY\",\"note\":\"$BATT_GUAGE_NOTE\"},\"mmc\":{\"detect\":\"$MMC_DETECT\",\"verify\":\"$MMC_VERIFY\",\"note\":\"$MMC_NOTE\"},\"camera\":{\"detect\":\"$CAM_DETECT\",\"model\":\"$CAM_MODEL\",\"verify\":\"$CAM_VERIFY\",\"note\":\"$CAM_NOTE\"},\"modem\":{\"detect\":\"$MODEM_DETECT\",\"verify\":\"$MODEM_VERIFY\",\"state\":\"$MODEM_STATE\",\"failed_reason\":\"$MODEM_FAILED_REASON\",\"signal\":\"$MODEM_SIGNAL\",\"note\":\"$MODEM_NOTE\"}}" > /tmp/somefile