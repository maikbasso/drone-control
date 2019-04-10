#!/user/bin/python

# @Author: Maik Basso <maik@maikbasso.com.br> 

import socket
import time

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
	if i == 10:	client.sendall('{"command": "setPosition", "args": {"x":-10,"y":10,"z":0}}')
	if i == 20:	client.sendall('{"command": "setPosition", "args": {"x":20,"y":0,"z":0}}')
	if i == 30:	client.sendall('{"command": "setPosition", "args": {"x":0,"y":-20,"z":0}}')
	if i == 40:	client.sendall('{"command": "setPosition", "args": {"x":-20,"y":0,"z":0}}')
	if i == 50:	client.sendall('{"command": "setPosition", "args": {"x":0,"y":20,"z":0}}')
	if i == 60:	client.sendall('{"command": "setPosition", "args": {"x":10,"y":-0,"z":0}}')
	if i == 70:	client.sendall('{"command": "backToLand", "args": {}}')
	if i == 80: 
		client.close()
		exit()
	time.sleep(1)