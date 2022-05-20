#! /bin/sh

DEVFILE="/tmp/somefile"
GPSFILE="/tmp/gps"
UPDATE_DURATION="120m"

get_loc () {
    printf "location func\n"
    # get last line of output in LOC
    LOC=$(echo -ne "AT+QGPSLOC?\r\n" | microcom -t 100 -X /dev/ttyUSB2 -s 115200 | awk 'END{print $(NF)}')
    if [ $LOC = "516" ]; then
        LOC_NOTE="location_not_set"
    elif [ $LOC = "OK" ]; then
        LAT=$(echo -ne "AT+QGPSLOC?\r\n" | microcom -t 100 -X /dev/ttyUSB2 -s 115200 | awk -F',' 'NR == 2 {print $2}')
        LONG=$(echo -ne "AT+QGPSLOC?\r\n" | microcom -t 100 -X /dev/ttyUSB2 -s 115200 | awk -F',' 'NR == 2 {print $3}')
        ALT=$(echo -ne "AT+QGPSLOC?\r\n" | microcom -t 100 -X /dev/ttyUSB2 -s 115200 | awk -F',' 'NR == 2 {print $5}')
        NSAT=$(echo -ne "AT+QGPSLOC?\r\n" | microcom -t 100 -X /dev/ttyUSB2 -s 115200 | awk -F',' 'NR == 2 {print $NF}')
    else
        echo ""
    fi
}

setup_gps () {  
    printf "setup func\n"
    # configure gps, maybe not needed
    CFG=$(echo -ne "AT+QGPSCFG=\"gpsnmeatype\",3\r\n" | microcom -t 100 -X /dev/ttyUSB2 -s 115200 | awk ' BEGIN{RS=""} {print $(NF)}')
    if [ -z "$CFG" ]; then
        CFG_NOTE="cmd_err"
    elif [ $CFG = "OK" ]; then
        CFG_NOTE="configured"
    else
        CFG_NOTE=$CFG
    fi

    # enable gps
    EN=$(echo -ne "AT+QGPS=1\r\n" | microcom -t 100 -X /dev/ttyUSB2 -s 115200 | awk 'BEGIN{RS=""} {print $(NF)}' )

    if [ -z "$EN" ]; then
        EN_NOTE="cmd_err"
    elif [ $EN = "OK" ]; then
        GPS_STATE="gps_enabled"
    else
        EN_NOTE=$EN
        GPS_STATE="err"
    fi
}

close_gps () {
    printf "closing func\n"
    DIS=$(echo -ne "AT+QGPSEND\r\n" | microcom -t 100 -X /dev/ttyUSB2 -s 115200 | awk 'END{print $NF}')
    
    if [ -z "$DIS" ]; then
        DIS_NOTE="cmd_err"
    elif [ $DIS = "OK" ]; then
        GPS_STATE="gps_disabled"
    else
        DIS_NOTE=$DIS
        GPS_STATE="err"
    fi
}

write_to_file () {
    # echo "{
    #         \"time\":\"$(date +"%Y-%m-%dT%H:%M:%S")\",
    #         \"gps_state\":\"$GPS_STATE\",
    #         \"config_info\":{
    #             \"config\":\"$CFG\",
    #             \"config_note\":\"$CFG_NOTE\"
    #         },
    #         \"open_info\":{
    #             \"enable\":\"$EN\",
    #             \"enable_note\":\"$EN_NOT\"
    #         },
    #         \"close_info\":{
    #             \"disable\":\"$DIS\",
    #             \"disable_note\":\"$DIS_NOTE\"
    #         },
    #         \"location\":{
    #             \"status\":\"$LOC\",
    #             \"latitude\":\"$LAT\",
    #             \"longitude\":\"$LONG\",
    #             \"altitude\":\"$ALT\",
    #             \"satellites\":\"$NSAT\"
    #         }
    #     }" > $GPSFILE

    echo "{
            \"time\":\"$(date +"%Y-%m-%dT%H:%M:%S")\",
            \"gps_state\":\"$GPS_STATE\",
            \"location\":{
                    \"status\":\"$LOC\",
                    \"latitude\":\"$LAT\",
                    \"longitude\":\"$LONG\",
                    \"altitude\":\"$ALT\",
                    \"satellites\":\"$NSAT\"
            }
    }" > $GPSFILE
}

if [ -f $DEVFILE ]; then
    MODEM=$(cat $DEVFILE | python3 -c "import sys, json; print(json.load(sys.stdin)['modem']['detect'])")
    if [ $MODEM = "true" ]; then
        while true; do
            setup_gps
            get_loc

            write_to_file
    
            while [[ $LOC = "516" || -z "$LOC" ]]; do
                printf "getting loc again\n"
                write_to_file
                get_loc
                sleep 2
            done

            close_gps
            write_to_file
            sleep ${UPDATE_DURATION}
        done
    else 
        printf "modem not detected\n"
        GPS_STATE="modem_not_found"
        write_to_file
        exit 1
    fi 
else
    printf "$DEVFILE not found\n"

fi