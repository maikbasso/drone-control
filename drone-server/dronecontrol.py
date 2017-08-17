#!/user/bin/python

# @Author: Maik Basso <maik@maikbasso.com.br>

from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil
import time
import json
import threading
import socket
import os
import math

class DroneControl:
	
	vehicle = None
	connected = False
	commands = list()
	threads = list()
	socketServer = None
	clients = list()

	# CONSTRUCTOR AND DESTRUCTOR

	def __init__(self, droneHost, droneBaud, socketHost, socketPort, socketMaxClients):
		print "*" * 36
		print "*** DroneControl is initialized! ***"
		print "*" * 36
		#connect to the drone
		self.conn(droneHost, droneBaud)
		#create the server socket
		self.createSocketServer(socketHost, socketPort, socketMaxClients)
		#runs all methoads assincronously
		self.threads.append(threading.Thread(target=self.waitingForClients))
		self.threads.append(threading.Thread(target=self.runCommands))
		#the program was initialized with success
		print "=> DroneControl is initialized!"
		#start all threads
		for t in self.threads:
			t.start()

	def __del__(self):
		self.disconnect()

	# CONNECTION METHODS
	
	def conn(self, host, baud):
		if self.vehicle is None:
			self.vehicle = connect(host, baud=baud, wait_ready=True)
			self.connected = True
			print "=> Connected to vehicle on -host:", host, "-baudrate:", baud

	def createSocketServer(self, host, port, maxClients):
		if self.socketServer is None:
			# create a TCP server
			self.socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			# Prepares server to wait for client connection
			self.socketServer.bind((host, port))
			# Listem the clients
			self.socketServer.listen(maxClients)
			print "=> Socket server is started on -host:", host, "-port:", port
			print "=> Allow connection for", maxClients, "clients."

	def disconnect(self):
		if self.connected is True:
			self.connected = False
			self.socketServer.close()
			self.vehicle.close()
			print "=> Disconnecting from the vehicle and closing the socket server."

	# COMMAND METHODS

	def waitingForClients(self):
		try:
			while self.connected == True:
				#print '=> Waiting for client connection...'
				conn, clientAddress = self.socketServer.accept()
				print '=> Client', clientAddress,'conected!'
				#create a Thread for each client
				clientThread = threading.Thread(target=self.receiveCommands, args=(conn, clientAddress,))
				clientThread.start()
				self.threads.append(clientThread)
				#print "=> Number of Threads:", len(self.threads)
		finally:
			self.socketServer.close()

	def receiveCommands(self, clientConn, clientAddress):
		while True:
			try:
				if clientConn is None:
					break
				else:
					message = clientConn.recv(200)
					print "===> Message:", message
					if len(message) > 0:
						cmd = json.loads(message)
						#print "=> Received command:", cmd
						self.commands.append(cmd)
						self.filterCommands()
					else:
						print "=> Client", clientAddress, "closed the connection."
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
					method = getattr(self, cmd["command"])
					method(cmd["args"])
				finally:
					pass

	# CLIENTS METHODS

	def registerClient(self, commandLine):
		self.clients.append(commandLine)

	def startClients(self):
		while self.connected is False:
			time.sleep(1)
		
		for commandLine in self.clients:
			t = threading.Thread(target=os.system, args=(commandLine,))
			t.start()
			self.threads.append(t)
			

	# ALL COMMANDS ARE IMPLEMENTED HERE!

	def printArgs(self, args):
		print "Command runs with args =", args

	def setSpeed(self, args):
		# Set airspeed using attribute
		self.vehicle.airspeed = args["airSpeed"] #m/s
		# Set groundspeed using attribute
		self.vehicle.groundspeed = args["groundSpeed"] #m/s

	def arm(self, args):
		print "Basic pre-arm checks"
		# Don't let the user try to arm until autopilot is ready
		while not self.vehicle.is_armable:
			print "Waiting for vehicle to initialise..."
			time.sleep(1)

		print "Arming motors"
		# Copter should arm in GUIDED mode
		self.vehicle.mode = VehicleMode("GUIDED")
		self.vehicle.armed = True

		while not self.vehicle.armed:
			print "Waiting for arming..."
			time.sleep(1)

	def takeOff(self, args):
		print "Taking off!"
		self.vehicle.simple_takeoff(args["z"])

	def backToLand(self, args):
		print "Back to the land"
		self.vehicle.mode = VehicleMode("LAND")

	def returnToLaunch(self, args):
		print "Return to launch"
		self.vehicle.mode = VehicleMode("RTL")

	def rotateGimbal(self, args):
		self.vehicle.gimbal.rotate(args["pitch"], args["roll"], args["yaw"])
		time.sleep(2)

	def setVelocity(self, args):		
		msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, 0, 0, # x, y, z positions (not used)
        args["velocity_x"], args["velocity_y"], args["velocity_z"], # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

		# send command to vehicle on 1 Hz cycle
		for x in range(0, args["duration"]):
			self.vehicle.send_mavlink(msg)
			time.sleep(1)

	def setPosition(self, args):
		original_location = self.vehicle.location.global_frame
		dNorth = args["y"]
		dEast = args["x"]
		alt = original_location.alt + args["z"]
		
		#Radius of "spherical" earth
		earth_radius=6378137.0
	    
	    #Coordinate offsets in radians
		dLat = dNorth/earth_radius
		dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

		#New position in decimal degrees
		newlat = original_location.lat + (dLat * 180/math.pi)
		newlon = original_location.lon + (dLon * 180/math.pi)
		if type(original_location) is LocationGlobal:
		    targetlocation=LocationGlobal(newlat, newlon, alt)
		elif type(original_location) is LocationGlobalRelative:
		    targetlocation=LocationGlobalRelative(newlat, newlon, alt)

		#go to new location
		self.vehicle.simple_goto(targetlocation)

	def getParameters(self, args):
		return self.vehicle.parameters

	def disableArmingCheck(self, args):
		print "Disable arming check"
		parameters["ARMING_CHECK"] = 0