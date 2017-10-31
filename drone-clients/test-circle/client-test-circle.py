#!/user/bin/python

# @Author: Maik Basso <maik@maikbasso.com.br> 

import socket
import time
import math

# Create a TCP/IP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
client.connect(('localhost', 7000))
i = 0
while True:
	i += 1
	if i == 1:	client.sendall('{"command": "arm", "args": {}}')
	if i == 2:	client.sendall('{"command": "setSpeed", "args": {"airSpeed": 7,"groundSpeed": 5}}')
	if i == 3:	client.sendall('{"command": "takeOff", "args": {"z": 10}}')
	if i == 10:
		#equation of the circle
		#x = r*cos(a*Pi/180), y = r*sin(a*Pi/180)
		r = 5
		for a in range(0,360):
			client.sendall('{"command": "setPosition", "args": {"x": %d,"y": %d,"z":0}}'%(r*math.cos(a*math.pi/180), r*math.sin(a*math.pi/180)))
			time.sleep(0.5)
	if i == 20:	client.sendall('{"command": "backToLand", "args": {}}')
	if i == 21: 
		client.close()
		exit()
	time.sleep(1)