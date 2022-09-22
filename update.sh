#!/bin/bash

# if [ $1=="revert" ]
# then

# cd /usr/sbin/device-manager/DeviceManager/templates/
# rm configurations.html
# mv configurations.html configuration.html.backup 

# cd /usr/sbin/device-manager/DeviceManager/
# rm app.py
# mv app.py app.py.backup

# exit 0
# fi

cd /usr/sbin/device-manager/DeviceManager/templates/
rm configurations.html.backup
mv configurations.html configurations.html.backup 
wget https://raw.githubusercontent.com/AWaDH-IIT-Ropar/testCode/atul/DeviceManager/templates/configurations.html
rm videoFeed.html.backup
mv videoFeed.html videoFeed.html.backup 
wget https://raw.githubusercontent.com/AWaDH-IIT-Ropar/testCode/atul/DeviceManager/templates/videoFeed.html
cd /usr/sbin/device-manager/DeviceManager/
rm app.py.backup
mv app.py app.py.backup
wget https://raw.githubusercontent.com/AWaDH-IIT-Ropar/testCode/atul/DeviceManager/app.py
cd /usr/sbin/device-manager/DeviceManager/static/css/
rm videoFeed.css.backup
mv videoFeed.css videoFeed.css.backup
wget https://raw.githubusercontent.com/AWaDH-IIT-Ropar/testCode/atul/DeviceManager/static/css/videoFeed.css

