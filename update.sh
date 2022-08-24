#!/bin/bash

if [ $1=="revert" ]
then

cd /usr/sbin/device-manager/DeviceManager/templates/
rm configurations.html
mv configurations.html configuration.html.backup 

cd /usr/sbin/device-manager/DeviceManager/
rm app.py
mv app.py app.py.backup

exit 0
fi

cd /usr/sbin/device-manager/DeviceManager/templates/
mv configurations.html configuration.html.backup 
wget https://raw.githubusercontent.com/AWaDH-IIT-Ropar/testCode/atul/DeviceManager/templates/configurations.html
cd /usr/sbin/device-manager/DeviceManager/
mv app.py app.py.backup
wget https://raw.githubusercontent.com/AWaDH-IIT-Ropar/testCode/atul/DeviceManager/app.py
