#!/user/bin/python

# @Author: Maik Basso <maik@maikbasso.com.br> 

import socket
import time
import math

# Create a TCP/IP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
client.connect(('localhost', 7000))
time.sleep(1)

#create auto-mission
client.sendall('{"command": "initAutoMission", "args": {"alt": 10}}')
time.sleep(1)

client.sendall('{"command": "addWayPointAutoMission", "args": {"lat": -30.076462, "lon": -51.118124, "alt": 10}}')
time.sleep(1)

client.sendall('{"command": "addWayPointAutoMission", "args": {"lat": -30.076449, "lon": -51.117063, "alt": 10}}')
time.sleep(1)

client.sendall('{"command": "startAutoMission", "args": {}}')
time.sleep(1)

#close client
client.close()
