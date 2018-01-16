#!/user/bin/python

# @Author: Maik Basso <maik@maikbasso.com.br>
# set parameter CBRK_USB_CHK = 197848
import time
import socket
import os
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil
from droneclient import DroneClient

class DroneControl:
	
	vehicle = None
	connected = False
	threads = list()
	socketServer = None
	clients = list()
	droneClients = list()

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
		#the program was initialized with success
		print "=> DC > It is initialized!"
		self.waitingForClients()

	def __del__(self):
		self.disconnect()

	# CONNECTION METHODS
	
	def conn(self, host, baud):
		if self.vehicle is None:
			self.vehicle = connect(host, baud=baud, wait_ready=True)
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
			for d in self.droneClients:
				d.setConnectionStatus(False)
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
				dc = DroneClient(self.vehicle, conn, clientAddress)
				self.droneClients.append(dc)
				print "=> DC > Number of Clients:", len(self.droneClients)
		finally:
			self.socketServer.close()

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
