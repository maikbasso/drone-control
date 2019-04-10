#!/user/bin/python

# @Author: Maik Basso <maik@maikbasso.com.br> 

import socket
import time
import json

# Create a TCP/IP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
client.connect(('localhost', 7000))

#register all comands
commands = {
	0:{"command": "arm","args":{}},
	1:{"command": "setSpeed","args":{"airSpeed": 0,"groundSpeed": 0}},
	2:{"command": "takeOff","args":{"z": 0}},
	3:{"command": "backToLand","args":{}},
	4:{"command": "returnToLaunch","args":{}},
	5:{"command": "rotateGimbal","args":{"pitch":0,"roll":0,"yaw":0}},
	6:{"command": "setVelocity","args":{"velocity_x":0,"velocity_y":0,"velocity_z":0,"duration":0}},
	7:{"command": "setPosition","args":{"x":0,"y":0,"z":0}},
}

while True:
	#print all command options
	print ">>> Allowed commands:"
	for i in commands:
		print i,":",commands[i]["command"]
	print "Others - Exit command shell."
	cmdId = int(raw_input('Select an option > '))
	#checks if cmdId is a valid option 
	if(cmdId in list(commands)):
		#get the command
		command = commands[cmdId]
		print ">>", command["command"], "selected."
		print ">> Define the command args:"
		#populate data in command
		for key in command["args"]:
			command["args"][key] = int(raw_input('"%s" = '%(key)))
		#send message to server
		print "Send command:", command
		client.sendall(json.dumps(command))
	else:
		client.close()
		exit()