#!/bin/sh
while true; do
    dmesg | grep "PM: suspend exit"
    if [ $? = 0 ]; then
        printf "Device resumed after suspend\n"
        break
    fi
    sleep 10
done

printf "Rebooting Device in 10s\n"
sleep 10
reboot
