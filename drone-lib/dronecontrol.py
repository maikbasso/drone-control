#!/user/bin/python

# @Author: Maik Basso <maik@maikbasso.com.br>
# set parameter CBRK_USB_CHK = 197848
import time
import json
import threading
import socket
import os
import math
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil
from dccommands import DCCommands

class DroneControl:
	
	vehicle = None
	connected = False
	commands = list()
	dccommands = None
	threads = list()
	socketServer = None
	clients = list()

	# CONSTRUCTOR AND DESTRUCTOR

	def __init__(self, droneHost, droneBaud, socketHost, socketPort, socketMaxClients):
		print ""
		print "*" * 20
		print "*** DroneControl ***"
		print "*" * 20
		#connect to the drone
		self.conn(droneHost, droneBaud)
		#create the server socket
		self.createSocketServer(socketHost, socketPort, socketMaxClients)
		#runs all methoads assincronously
		self.threads.append(threading.Thread(target=self.waitingForClients))
		self.threads.append(threading.Thread(target=self.runCommands))
		#the program was initialized with success
		print "=> DC > It is initialized!"
		#start all threads
		for t in self.threads:
			t.start()

	def __del__(self):
		self.disconnect()

	# CONNECTION METHODS
	
	def conn(self, host, baud):
		if self.vehicle is None:
			self.vehicle = connect(host, baud=baud, wait_ready=True)
			self.dccommands = DCCommands(self.vehicle)
			self.connected = True
			print "=> DC > Connected to vehicle on -host:", host, "-baudrate:", baud

	def createSocketServer(self, host, port, maxClients):
		if self.socketServer is None:
			# create a TCP server
			self.socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			# Prepares server to wait for client connection
			self.socketServer.bind((host, port))
			# Listem the clients
			self.socketServer.listen(maxClients)
			print "=> DC > Socket server is started on -host:", host, "-port:", port
			print "=> DC > Allow connection for", maxClients, "clients."

	def disconnect(self):
		if self.connected is True:
			self.connected = False
			self.socketServer.close()
			self.vehicle.close()
			print "=> DC > Disconnecting from the vehicle and closing the socket server."

	# COMMAND METHODS

	def waitingForClients(self):
		try:
			while self.connected == True:
				#print "=> DC > Waiting for client connection..."
				conn, clientAddress = self.socketServer.accept()
				print "=> DC > Client", clientAddress,'conected!'
				#create a Thread for each client
				clientThread = threading.Thread(target=self.receiveCommands, args=(conn, clientAddress,))
				clientThread.start()
				self.threads.append(clientThread)
				print "=> DC > Number of Threads:", len(self.threads)
		finally:
			self.socketServer.close()

	def receiveCommands(self, clientConn, clientAddress):
		while True:
			try:
				if clientConn is None:
					break
				else:
					message = clientConn.recv(120)
					print "=> DC > received message:", message
					if len(message) > 0:
						cmd = json.loads(message)
						print "=> DC > message decode:", cmd
						self.commands.append([cmd, clientConn, clientAddress])
						self.filterCommands()
					else:
						print "=> DC > Client", clientAddress, "closed the connection."
						clientConn.close()
						clientConn = None
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
					cmd = self.commands[0]
					#remove the first command from list
					self.commands.remove(cmd)
					#select and execute method by command
					method = getattr(self.dccommands, cmd[0]["command"])
					response = method(cmd[0]["args"])
					print "=> DC > Running command:", cmd[0]
					#send the response to the client
					if response != None:
						# !!!!!!!! test if message is send from all or specifc client !!!!!!!!
						cmd[1].send(response)
						print "=> DC > Sending response:", response, "to client:", cmd[1]
					time.sleep(1)
				finally:
					pass

	# CLIENTS METHODS

	def registerClient(self, commandLine):
		self.clients.append(commandLine)
		print "=> DC > client registred:", commandLine

	def startClients(self):
		while self.connected is False:
			time.sleep(1)
		
		for commandLine in self.clients:
			t = threading.Thread(target=os.system, args=(commandLine,))
			t.start()
			self.threads.append(t)
			print "=> DC > client started:", commandLine
