weather () {
    if [ -f "/tmp/light_intensity" ]; then
        LUX=$(cat /tmp/light_intensity | awk -F':' '{print $2}')
    else
        printf "/tmp/light_intensity not found\n"
    fi

    if [ -f "/tmp/met" ]; then 
        HUMIDITY=$(cat /tmp/met | awk -F':' 'NR == 1 {print $2}')
        TEMPERATURE=$(cat /tmp/met | awk -F':' 'NR == 2 {print $2}')
    else    
        printf "/tmp/met not found\n"
    fi
    FILEPATH=${STORAGE_PATH}weather_$(date +"%d-%m-%Y_%H")_$SERIALID.csv
    echo $FILEPATH

    if [ -f $FILEPATH ]; then
        echo "$(date +"%d-%m-%Y,%H:%M:%S"),$LUX,$HUMIDITY,$TEMPERATURE" >> $FILEPATH
    else
        touch $FILEPATH
        echo "Date,Time,Lux,Humidity,TempC" > $FILEPATH
    fi
}

if [ -f "/etc/entomologist/ento.conf" ]; then
    SERIALID=$(cat /etc/entomologist/ento.conf | awk '/SERIAL_ID/ {print $2}' | tr -d '"' | tr -d ',')
    STORAGE_PATH=$(cat /etc/entomologist/ento.conf | awk '/STORAGE_PATH/ {print $2}' | tr -d '"' | tr -d ',')
    while true; do
        weather
        sleep 30
    done
else
    printf "/etc/entomologist/ento.conf not found\n"
fi