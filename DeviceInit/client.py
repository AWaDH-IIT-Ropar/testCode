#!/usr/bin/env python3

import socket
import threading
import json
import time

PORT = 9999
SERVER = "localhost"
ADDR = (SERVER, PORT)
STOP_BLINKING_MESSAGE = "STOP"

# Temporary function to imitate network status.
def network_status():
	with open('file.json') as f:
		content = json.loads(f.read())
		if content['status'] == 'False':
			return False
		else: 
			return True


class SocketClient:
  def __init__(self, service_name):
    self.service_name = service_name
    self.client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.client.connect(ADDR)

  def blink_led(self):
    ''' Fucntion to initate blinking of LED'''
    message = self.service_name.encode('utf-8')
    self.client.send(message)

  def stop_blink_led(self):
    ''' Function to stop LED blinking'''
    message = STOP_BLINKING_MESSAGE.encode('utf-8')
    self.client.send(message)

class DeviceInit:

  def network_check(self):

    if not network_status():

      # Creating network socket object to communicate with LED socket.
      network_client = SocketClient("network")
    	
      # Checking network status.
      while not network_status():
        network_client.blink_led()
        time.sleep(1)

      # Stopping LED blinking and closing network socket client from LED socket side.
      network_client.stop_blink_led()

device_check = DeviceInit()
device_check.network_check()