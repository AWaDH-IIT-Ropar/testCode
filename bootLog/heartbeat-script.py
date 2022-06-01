'''
@author: Rohit Sharma, Pratyush Verma
Date:07/01/2022
'''

import paho.mqtt.client as mqtt
import json
import requests
import ssl
import time
from datetime import datetime

path=(__file__).split('/')
path.pop()
path="/".join(path)
path='/home/awadh/Downloads/air-quality-aws/'

print(path)

#IoT_protocol_name = "x-amzn-mqtt-ca"
mqtt_url = "a33enhgkqb6z8i-ats.iot.us-west-2.amazonaws.com"
root_ca = path+'AmazonRootCA1.pem'
public_crt = path+'certificate.pem.crt'
private_key = path+'private.pem.key'

def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connected to MQTT broker!")
		
	else:
		print("Bad connection: Failed to connect!", rc)


def publishData(client):
	global boot_status
	topic = "digital_entomologist/D00201/status"
	
	now = datetime.now() 
	timestamp = now.strftime("%d/%m/%Y, %H:%M:%S")


	heartbeat={
		"DeviceName": "Digital Entomologist",
		"DeviceID": "D00200",
		"Status": "Heartbeat",
		"Timestamp" : timestamp,
		}

	boot_notification={
		"DeviceName": "Digital Entomologist",
		"DeviceID": "D00200",
		"Status" : "Boot",
		"Timestamp" : timestamp,
		}
    
	try:
		
		requests.head('http://www.google.com/', timeout=3) 
		
		data_heartbeat = json.dumps(heartbeat)  #converting 'msg' into json
		data_notification = json.dumps(boot_notification) #converting 'msg' into json
		
		if boot_status == 0:
			client.publish(topic, data_notification, qos=1)
			time.sleep(30)
			boot_status +=1
			print(boot_status)
			print("Boot")

		if boot_status !=0:
			client.publish(topic, data_heartbeat, qos=1)  #publish data on server
			time.sleep(30)
			print(boot_status)        
		
		return True

	except requests.ConnectionError as ex:
		print("Connection Lost! Please wait for some time...")
		return False

if __name__ == "__main__":
	global boot_status
	boot_status =0
	client = mqtt.Client()
	# methods call
	client.tls_set(root_ca,
				certfile = public_crt,
				keyfile = private_key,
				cert_reqs = ssl.CERT_REQUIRED,
				tls_version = ssl.PROTOCOL_TLSv1_2,
				ciphers = None)
	client.on_connect = on_connect
	client.connect(mqtt_url, port = 8883, keepalive=60)
	client.loop_start()

	while True:
		#print(dt)
		#method call

		publishData(client)
