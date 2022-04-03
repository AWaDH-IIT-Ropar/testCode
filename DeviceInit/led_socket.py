#!/usr/bin/env python3
import socket
import threading

# CONSTANTS

PORT = 9999
SERVER = 'localhost'
ADDR = (SERVER, PORT)


class LEDSocket:
  def __init__(self):

    # Creating an object of server and port.
    self.ADDR = ADDR
    
    # Creating LED socket object.  
    self.led_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def start_socket(self):

    # Binding Socket connection to server via port.
    self.led_server.bind(ADDR)

    # Starts listening to connections on this socket. 
    # Also restricitng it to only 1 connection. It won't listen to another connection.
    self.led_server.listen(1)
    print("[SERVER] Started Listening for new connections.")

    while True:
      conn, addr = self.led_server.accept() # This line is a blocking code.
      print(f"[NEW CONNECTION] {addr}")
      self.led_blink_handler(conn, addr)

  def led_blink_handler(self, conn, addr):
    
    connected = True
    while connected:
      msg = conn.recv(1024).decode('utf-8') # Here 1024 is the buffer size for the text to be received in bytes.
      if msg:
        
        print(f"[CLIENT:{addr}] {msg}")

        if msg == "STOP":
          connected = False
    conn.close()	


ls = LEDSocket()
print("Starting Socket")
ls.start_socket()

