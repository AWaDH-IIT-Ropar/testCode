#!/usr/bin/env python3

'''
@author: Tabish Naved
Date: 04-Aug-2022
Description: This script will generate new certificates for the IoT thing.
It also revokes the old certificates from cloud as well as the local device.
'''

import paho.mqtt.client as mqtt
from shutil import copyfile
import json
import sys
import os

class CreateNewCertificate():

	def __init__(self, thingName, rootCA, thingCertificate, privateKey):

		# Setting MQTT client.
		self.thingName = thingName
		self.client = mqtt.Client(thingName)
		self.client.tls_set(rootCA, thingCertificate, privateKey)

		# Setting Old Certificate Path.
		self.oldRootCertPath = rootCA

		self.newCertificatePubTopic = f'manage/{thingName}/rotateCertificate'
		self.newCertificateSubTopic = f'manage/{thingName}/newCertificate'
		
		self.END_POINT = '' # Place AWS ARN here
		self.KEEP_ALIVE_INTERVAL = 44
		self.PORT = 8883
		self.PUBLISH_QoS = 1
		self.SUBSCRIBE_QoS = 0

	# Callback Functions
	def on_connect(self, client, userdata, flags, rc):
		if rc == 0:
			print(f'[{self.thingName}]: Connection Established!')
			self.client.subscribe(self.newCertificateSubTopic, self.SUBSCRIBE_QoS)
		else:
			print(f'[{self.thingName}]: Bad Connection')
			sys.exit(1)

	def on_publish(self, client, userdata, flags):
		print(f'[{self.thingName}]: Request for new certificate published.')

	def on_subscribe(self, client, userdata, mid, granted_qos):
		print(f'[{self.thingName}]: Subscribed for recieving new certificate data.')
		payload = {
		'ThingName' : self.thingName
		}
		self.client.publish(self.newCertificatePubTopic, json.dumps(payload), self.PUBLISH_QoS)

	def on_message(self, client, userdata, message):
		response = json.loads(message.payload.decode('utf-8'))
		# print(response)
		print(f'[{self.thingName}]: New Certificates Recieved!')

		self.save_certificates_to_path(response)
		self.client.disconnect()

	def run(self):
		self.client.on_connect = self.on_connect
		self.client.on_publish = self.on_publish
		self.client.on_subscribe = self.on_subscribe
		self.client.on_message = self.on_message

		self.client.connect(self.END_POINT, self.PORT, self.KEEP_ALIVE_INTERVAL)
		self.client.loop_forever()


	# Fucntion to save new certificaytes to path
	def save_certificates_to_path(self, cert_resp):
		# print(cert_resp)
		# Creating a new Directory for new certificates.
		parentPath = os.getcwd()
		newDirectory = 'newCert'

		newPath = os.path.join(parentPath, newDirectory)
		try:
			os.mkdir(newPath)
		except FileExistsError:
			pass

		# Saving Certificate Id
		certificateInfo = {
			'certificateId' : cert_resp['certificateId'],
			'certificateArn' : cert_resp['certificateArn']
		}
		with open(os.path.join(newPath,'certificateInfo.json'), 'w') as f:
			f.write(json.dumps(certificateInfo))
			f.close()


		# Copying RootCA from old path to new path.
		filename = self.oldRootCertPath.split('/')[-1]
		newRootCertPath = os.path.join(newPath, filename)
		copyfile(self.oldRootCertPath, newRootCertPath)

		# Saving Thing Certificate
		with open(os.path.join(newPath,'D01299-certificate.pem.crt'), 'w') as f:
			f.write(cert_resp['certificatePem'])
			f.close()

		# Saving Thing Private Key
		with open(os.path.join(newPath,'D01299-private.pem.key'), 'w') as f:
			f.write(cert_resp['keyPair']['PrivateKey'])
			f.close()

	


if __name__ == '__main__':

	thingName = "CameraDevice_D01299"
	rootCA = 'certificates_D01299/AmazonRootCA1.pem'
	thingCertificate = 'certificates_D01299/D01299-certificate.pem.crt'
	privateKey = 'certificates_D01299/D01299-private.pem.key'

	newCertificate = CreateNewCertificate(thingName, rootCA, thingCertificate, privateKey)
	newCertificate.run()


# newCertificate.save_certificates_to_path(payload)
