#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import datetime as dt
import subprocess
import random
import json
import sys
import socket
import ast
import time
import datetime
import os
import multiprocessing
#import logging as log

with open(f"ento.conf",'r') as file:
#with open(f"/etc/entomologist/ento.conf",'r') as file:
	data=json.load(file)
provisionstatus=data["device"]["PROVISION_STATUS"]
DEVICE_SERIAL_ID = data["device"]["SERIAL_ID"]

MQTT_BROKER = data["device"]["ENDPOINT_URL"]
PORT = 8883
MQTT_KEEP_INTERVAL = 44
# rootCA = '/etc/entomologist/cert/AmazonRootCA1.pem'
# cert = '/etc/entomologist/cert/certificate.pem.crt'
# privateKey = '/etc/entomologist/cert/private.pem.key'
rootCA = 'AmazonRootCA1.pem'
cert = 'certificate.pem.crt'
privateKey = 'private.pem.key'

#BUCKET_NAME = "test-entomoligist"

# Publish Details

PUBLISH_CLIENT_NAME = f'{DEVICE_SERIAL_ID}_Boot_Log_Client'
PUBLISH_TOPIC = f'de/boot/{DEVICE_SERIAL_ID}'
PUBLISH_QoS = 1

def on_publish(client, userdata, message):

	print("Boot log details published to topic.\n\nDisconnecting from publish client...\n")
	client.disconnect()

def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Boot Publish Client Connected")
		client.publish(TOPIC, PAYLOAD, QoS)
		
	else:
		print("Bad connection: Boot Publish Client")


def start_publish(broker, port, interval, clientName, topic, qos, payload, rootCA, cert, privateKey):

	global TOPIC
	global QoS
	global PAYLOAD

	TOPIC = topic
	QoS = qos
	PAYLOAD = payload

	time.sleep(1)
	# AWS Publishing Cient
	pubClient = mqtt.Client(clientName)

	# Setting Certificates
	pubClient.tls_set(rootCA, cert, privateKey)

	# Callback functions
	pubClient.on_connect = on_connect
	pubClient.on_publish = on_publish
	
	# Connecting to broker and publishing payload.
	while True:
		try:
			pubClient.connect(broker, port, interval)
			break
		except Exception as e:
			# Write the loggoing code here.
			print("I ran in exception: pubclient connect")
			print(e)
			time.sleep(5)
	

	#pubClient.loop_forever()
	pubClient.loop_start()
	time.sleep(5)
	pubClient.loop_stop()

def generate_payload():

	with open(f"/tmp/gps",'r') as file:
		data_gps=json.load(file)

	with open(f"/tmp/battery_parameters",'r') as file:
		data_battery=json.load(file)

	with open(f"/tmp/met",'r') as file:
		data_met=json.load(file)

	with open(f"/tmp/light_intensity",'r') as file:
		data_light=json.load(file)

	bootTime=str(datetime.datetime.now())
	payload = {
		"timestamp":bootTime,
		"deviceid":DEVICE_SERIAL_ID,
		"gps": data_gps,
		"battery": data_battery,
		"temp": data_met,
		"light": data_light
	}
	print(bootTime)
	print(payload)
	return json.dumps(payload)

def main():
	bootTime=str(datetime.datetime.now())
	time.sleep(2)
	while 1:
		with open(f"ento.conf",'r') as file:
		#with open(f"/etc/entomologist/ento.conf",'r') as file:
			data=json.load(file)
		provisionstatus=data["device"]["PROVISION_STATUS"]
		if provisionstatus=="True":
			break
		time.sleep(5)
	PAYLOAD=generate_payload()
	start_publish(MQTT_BROKER,PORT,MQTT_KEEP_INTERVAL,PUBLISH_CLIENT_NAME,PUBLISH_TOPIC,PUBLISH_QoS,PAYLOAD,rootCA,cert,privateKey)

main()
