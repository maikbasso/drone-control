#!/user/bin/python

# @Author: Maik Basso <maik@maikbasso.com.br>

import time
import json
import threading
import socket
import os
import math
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil
from dccommands import DCCommands

class DroneClient:
	
	vehicle = None
	#connected = False
	#commands = None
	#dccommands = None

	# CONSTRUCTOR AND DESTRUCTOR

	def __init__(self, vehicle, conn, clientAddress):
		self.connected = True
		self.commands = list()
		self.vehicle = vehicle
		self.dccommands = DCCommands(self.vehicle)
		t1 = threading.Thread(target=self.receiveCommands, args=(conn, clientAddress,))
		t2 = threading.Thread(target=self.runCommands)
		t1.start()
		t2.start()	

	def __del__(self):
		pass

	def setConnectionStatus(self, status):
		self.connected = status

	def receiveCommands(self, clientConn, clientAddress):
		while self.connected == True:
			try:
				if clientConn is None:
					break
				else:
					message = clientConn.recv(120)
					print "=> DC > received message:", message
					if len(message) > 0:
						try:
							cmd = json.loads(message)
							print "=> DC > message decode:", cmd
							self.commands.append([cmd, clientConn, clientAddress])
							self.filterCommands()
						except:
							# Error parsing json message
							clientConn.sendall('{"command": "response", "args": {"status": "false", "message": "Error parsing json message."}')
						finally:
							pass
					else:
						print "=> DC > Client", clientAddress, "closed the connection."
						clientConn.close()
						clientConn = None
						self.connected = False
			finally:
				pass

	def filterCommands(self):
		# Not necessary, Pixhawk itself takes care of it
		pass

	def runCommands(self):
		while self.connected == True:
			if len(self.commands) > 0:
				try:
					#get the first command
					cmd0 = self.commands[0]
					cmd = cmd0[:]
					#remove the first command from list
					self.commands.remove(cmd0)
					#select and execute method by command
					method = getattr(self.dccommands, cmd[0]["command"])
					response = method(cmd[0]["args"])
					#print "=> DC >", cmd[1], "> Running command:", cmd[0]
					print "=> DC > Running command:", cmd[0]
					#send the response to the client
					if response != None:
						# !!!!!!!! test if message is send from all or specifc client !!!!!!!!
						cmd[1].send(response)
						print "=> DC > Sending response:", response, "to client:", cmd[1]
					time.sleep(1)
				finally:
					pass
