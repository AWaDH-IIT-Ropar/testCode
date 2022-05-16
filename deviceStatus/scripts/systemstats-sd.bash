#!/bin/sh

function general_info () {
    # reading board serial number and deleting any null character in it
    BRD_SERIAL_NUM=$(tr -d '\0' </sys/firmware/devicetree/base/serial-number)
} # done

function get_cpu () {
    CORE_A53_TEMP=$(echo "scale=2 ; $(cat /sys/class/thermal/thermal_zone0/temp) / 1000" | bc -l)
    CORE_A72_TEMP=$(echo "scale=2 ; $(cat /sys/class/thermal/thermal_zone1/temp) / 1000" | bc -l)

    read -r CPU_USAGE_A53_0 CPU_USAGE_A53_1 CPU_USAGE_A53_2 CPU_USAGE_A53_3 CPU_USAGE_A72_0 CPU_USAGE_A72_1 <<< $(python3 -c "import psutil; print(psutil.cpu_percent(percpu=True))" | awk -F',' '{print $1 $2 $3 $4 $5 $6}')
    
    CPU_USAGE_A53_0=${CPU_USAGE_A53_0:1}
    CPU_USAGE_A53_1=0
    CPU_USAGE_A53_2=0
    CPU_USAGE_A53_3=0
    CPU_USAGE_A72_0=0
    CPU_USAGE_A72_1=${CPU_USAGE_A72_1::-1}

    local TMP=$(echo "($CPU_USAGE_A53_0 + $CPU_USAGE_A53_1 + $CPU_USAGE_A53_2 + $CPU_USAGE_A53_3 + $CPU_USAGE_A72_0 + $CPU_USAGE_A72_1) / 2" | bc -l)
    CPU_USAGE=$TMP
} # not done

function get_gpu () {
    # calculate GPU temperatures
    GPU_0_TEMP=$(echo "scale=2 ; $(cat /sys/class/thermal/thermal_zone2/temp) / 1000" | bc -l)
    GPU_1_TEMP=$(echo "scale=2 ; $(cat /sys/class/thermal/thermal_zone3/temp) / 1000" | bc -l)

    # calculate GPU metrics
    local GPU_FREE=$(cat /sys/kernel/debug/gc/meminfo | awk 'NR == 3 {print $3}')
    local GPU_USED=$(cat /sys/kernel/debug/gc/meminfo | awk 'NR == 4 {print $3}')
    local GPU_TOTAL=$(cat /sys/kernel/debug/gc/meminfo | awk 'NR == 7 {print $3}')

    local GPU_PERCENT_TMP=$(echo "( $GPU_USED / $GPU_TOTAL ) * 100 " | bc -l) # temporary variable
    GPU_USAGE=$(printf %.3f $GPU_PERCENT_TMP)
} # done

function get_ram () {
    # calculate RAM metrics
    RAM_TOTAL=$(printf %.3f $(echo "$(free | awk 'NR == 2 {print $2}') / (1024*1024)" | bc -l))
    RAM_FREE=$(printf %.3f $(echo "$(free | awk 'NR == 2 {print $4}') / (1024*1024)" | bc -l))
    local RAM_USED=$(printf %.3f $(echo "$(free | awk 'NR == 2 {print $3}') / (1024*1024)" | bc -l))
    local RAM_SHARED=$(printf %.3f $(echo "$(free | awk 'NR == 2 {print $5}') / (1024*1024)" | bc -l))
    local RAM_CACHE=$(printf %.3f $(echo "$(free | awk 'NR == 2 {print $6}') / (1024*1024)" | bc -l))

    local TMP=$(echo "( ( $RAM_USED + $RAM_SHARED + $RAM_CACHE ) / $RAM_TOTAL ) * 100 " | bc -l) # temporary variable
    RAM_USAGE=$(printf %.3f $TMP)
} # done

function get_connectivity () {
    # check internet connectivity
    wget -q --spider http://google.com 

    if [ $? -eq 0 ]; then 
        NETWORK_CONNECTED="true"
    else
        NETWORK_CONNECTED="false"
    fi 

    # get signal value
    NETWORK_SIGNAL=$(mmcli -m 0 | awk '/signal quality/ {print $4}') 
    NETWORK_SIGNAL=${NETWORK_SIGNAL::-1}
} # done

function get_data () {
    # get usage for ethernet
    DATA_ETH0_RX=$(printf %.3f $(echo "$(vnstat -i eth0 --xml m | awk -F'[<>]' '/<total>/ {print $5}') / (1024*1024)" | bc -l))
    DATA_ETH0_TX=$(printf %.3f $(echo "$(vnstat -i eth0 --xml m | awk -F'[<>]' '/<total>/ {print $9}') / (1024*1024)" | bc -l))

    # get usage for wwan
    # bug if iterface not found will throw a error on stderr and variables will remain empty
    DATA_WWAN0_RX=$(printf %.3f $(echo "$(vnstat -i wwan0 --xml m | awk -F'[<>]' '/<total>/ {print $5}') / (1024*1024)" | bc -l))
    DATA_WWAN0_TX=$(printf %.3f $(echo "$(vnstat -i wwan0 --xml m | awk -F'[<>]' '/<total>/ {print $9}') / (1024*1024)" | bc -l))
} # done

function get_power () {
    if [ -f "/tmp/battery_parameters" ]; then
        BATT_TEMP=$(cat /tmp/battery_parameters | awk 'NR == 1 {print $3}')
    
        local TMP=$(echo "$(cat /tmp/battery_parameters | awk 'NR == 2 {print $3}') / 1000" | bc -l) # temporary variable
        BATT_VOLTAGE=$(printf %.3f $TMP)

        local TMP=$(echo "$(cat /tmp/battery_parameters | awk 'NR == 3 {print $4}') / 1000" | bc -l) # temporary variable
        BATT_AVG_CURRENT=$(printf %.3f $TMP)

        local TMP=$(echo "$(cat /tmp/battery_parameters | awk 'NR == 4 {print $3}') / 1000" | bc -l) # temporary variable
        BATT_CURRENT=$(printf %.3f $TMP)
    else
        printf "/tmp/battery_parameters not found\n"
        BATT_TEMP=-1
        BATT_VOLTAGE=-1
        BATT_AVG_CURRENT=-1
        BATT_CURRENT=-1
    fi
} # done

function get_weather () {
    if [ -f "/tmp/light_intensity" ]; then
        W_LUX=$(cat /tmp/light_intensity | awk -F':' '{print $2}')
    else
        printf "/tmp/light_intensity not found"
        W_LUX=-1
    fi

    if [ -f "/tmp/met" ]; then
        W_TEMPERATURE=$(cat /tmp/met | awk -F':' 'NR == 2 {print $2}')
        W_HUMIDITY=$(cat /tmp/met | awk -F':' 'NR == 1 {print $2}')
    else
        printf "/tmp/met not found"
        W_TEMPERATURE=-1
        W_HUMIDITY=-1
    fi

} # done

while true; do

    general_info
    get_cpu
    get_gpu
    get_ram
    get_connectivity
    get_data
    get_power
    get_weather

    echo "{
        \"time\":\"$(date +"%Y-%m-%dT%I:%M:%S")\",
        \"cpuInfo\":{
            \"temperatures\":{
                \"A53\":$CORE_A53_TEMP,
                \"A72\":$CORE_A72_TEMP
            },
            \"usage\":$CPU_USAGE,
            \"usageDetailed\":{
                \"A53-0\":$CPU_USAGE_A53_0,
                \"A53-1\":$CPU_USAGE_A53_1,
                \"A53-2\":$CPU_USAGE_A53_2,
                \"A53-3\":$CPU_USAGE_A53_3,
                \"A72-0\":$CPU_USAGE_A72_0,
                \"A72-1\":$CPU_USAGE_A72_1
            }
        },
        \"gpuInfo\":{
            \"cores\":2,
            \"temperatures\":{
                \"GPU0\":$GPU_0_TEMP,
                \"GPU1\":$GPU_1_TEMP
            },
            \"memoryUsage\":$GPU_USAGE
        },
        \"ramInfo\":{
            \"total\":$RAM_TOTAL,
            \"usage\":$RAM_USAGE,
            \"free\":$RAM_FREE
        },
        \"generalInfo\":{
            \"board-serial\":$BRD_SERIAL_NUM,
        },
        \"internet\":{
            \"connectivity\":$NETWORK_CONNECTED,
            \"signal\":$NETWORK_SIGNAL
        },
        \"dataInfo\":{
            \"ethernet\":{
                \"rx\":$DATA_ETH0_RX,
                \"tx\":$DATA_ETH0_TX
            },
            \"wwan\":{
                \"rx\":$DATA_WWAN0_RX,
                \"tx\":$DATA_WWAN0_TX
            }
        },
        \"powerInfo\":{
            \"battery_temp\":$BATT_TEMP,
            \"voltage\":$BATT_VOLTAGE,
            \"avg_current\":$BATT_AVG_CURRENT,
            \"current\":$BATT_CURRENT
        }
    }" > /var/tmp/devicestats

    if [ -f "/media/mmcblk1p1/devicestats-bash.csv" ]; then
        echo "$(date +%Y-%m-%d,%I:%M:%S),$BATT_TEMP,$BATT_VOLTAGE,$BATT_AVG_CURRENT,$BATT_CURRENT,$CPU_USAGE,$CORE_A53_TEMP,$CPU_USAGE_A53_0,$CPU_USAGE_A53_1,$CPU_USAGE_A53_2,$CPU_USAGE_A53_3,$CORE_A72_TEMP,$CPU_USAGE_A72_0,$CPU_USAGE_A72_1,$GPU_0_TEMP,$GPU_1_TEMP,$GPU_USAGE,$RAM_USAGE,$DATA_ETH0_RX,$DATA_ETH0_TX,$DATA_WWAN0_RX,$DATA_WWAN0_TX" >> /media/mmcblk1p1/devicestats.csv
    else
        echo "Date,Time,Batt-temp,Voltage,Avg-current,Current,CPU-usage,A53-temp,A53-0-usage,A53-1-usage,A53-2-usage,A53-3-usage,A72-temp,A72-0-usage,A72-1-usage,GPU0-temp,GPU1-temp,GPU-usage,RAM-usage,Ethernet-RX,Ethernet-TX,WWAN-RX,WWAN-TX" > /media/mmcblk1p1/devicestats.csv
    fi
    sleep 60
done