#!/usr/bin/env python3

'''
@author: Tabish Naved
Date: 04-Aug-2022
Description: This script revoke the old certificates for the IoT thing.
Revoking involves - deactivating the certificate, detaching policies, detaching certifcate from thing and deleting the certificate.
'''

import paho.mqtt.client as mqtt
import json
import sys
import os

class RevokeOldCertificate():

	def __init__(self, thingName, rootCA, thingCertificate, privateKey, newCertificateArn):


		self.thingName = thingName
		self.client = mqtt.Client(thingName)
		self.client.tls_set(rootCA, thingCertificate, privateKey)

		
		self.oldRootCertPath = rootCA

		self.oldCertificatePubTopic = f'manage/{thingName}/revokeCertificate'
		self.oldCertificateSubTopic = f'manage/{thingName}/revokeSuccess'

		self.newCertificateArn = newCertificateArn
		self.END_POINT = '' # Place AWS ARN here
		self.KEEP_ALIVE_INTERVAL = 44
		self.PORT = 8883
		self.PUBLISH_QoS = 1
		self.SUBSCRIBE_QoS = 0

	# Callback Functions
	def on_connect(self, client, userdata, flags, rc):
		if rc == 0:
			print(f'[{self.thingName}]: Connection Established!')
			self.client.subscribe(self.oldCertificateSubTopic, self.SUBSCRIBE_QoS)
		else:
			print(f'[{self.thingName}]: Bad Connection')
			sys.exit(1)

	def on_publish(self, client, userdata, flags):
		print(f'[{self.thingName}]: Request made for revoking old certificate.')

	def on_subscribe(self, client, userdata, mid, granted_qos):
		print(f'[{self.thingName}]: Successfully subscribed.')
		payload = {
		'ThingName' : self.thingName,
		'certificateArn' : self.newCertificateArn
		}
		self.client.publish(self.oldCertificatePubTopic, json.dumps(payload), self.PUBLISH_QoS)

	def on_message(self, client, userdata, message):
		response = json.loads(message.payload.decode('utf-8'))
		self.client.disconnect()
		if response['body'] == 'True':
			print(f'[{self.thingName}]: Old Certificate revoked successfully!!')
			self.delete_old_certificate()
		

	def delete_old_certificate(self):
		currentPath = os.getcwd()
		
		oldRootCertPathList = self.oldRootCertPath.split('/')
		oldCertDirectory = '/'.join(oldRootCertPathList[:len(oldRootCertPathList)-1])

		currentPath = os.path.join(currentPath, oldCertDirectory)

		for file in os.listdir(currentPath):
			os.remove(os.path.join(currentPath, file))

		os.rmdir(currentPath)
		os.rename(os.path.join(os.getcwd(), 'newCert'), os.path.join(currentPath))
		print(f'[{self.thingName}]: Successfully replaced old certificates with new!')

	def run(self):
		self.client.on_connect = self.on_connect
		self.client.on_publish = self.on_publish
		self.client.on_subscribe = self.on_subscribe
		self.client.on_message = self.on_message

		self.client.connect(self.END_POINT, self.PORT, self.KEEP_ALIVE_INTERVAL)
		self.client.loop_forever()
	

# print(certtificateArn)
if __name__ == '__main__':
	thingName = "CameraDevice_D01299"
	rootCA = 'certificates_D01299/AmazonRootCA1.pem'
	thingCertificate = 'certificates_D01299/D01299-certificate.pem.crt'
	privateKey = 'certificates_D01299/D01299-private.pem.key'

	with open('newCert/certificateInfo.json') as f:
		certificateInfo = json.loads(f.read())
		certtificateArn = certificateInfo['certificateArn']

	revokeCertificate = RevokeOldCertificate(thingName, rootCA, thingCertificate, privateKey, certtificateArn)
	revokeCertificate.run()


# newCertificate.save_certificates_to_path(payload)
