#!/user/bin/python

# @Author: Maik Basso <maik@maikbasso.com.br>

import time
import math
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative, Command
from pymavlink import mavutil
import json
import logging
from time import gmtime, strftime

class DCCommands:
	
	vehicle = None
	autoCmds = None
	autoCmdsCount = 0
	lastAutoCmd = None
	frameworkTestsLog = None

	# CONSTRUCTOR AND DESTRUCTOR

	def __init__(self, vehicle):
		self.vehicle = vehicle

	def __del__(self):
		pass

	# to set PX4 Fligth Mode
	def PX4setMode(self, mavMode):
		print "=> DC Commands > Set PX4 flight mode to GUIDED"
		vehicle._master.mav.command_long_send(vehicle._master.target_system, vehicle._master.target_component, mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0, mavMode, 0, 0, 0, 0, 0, 0)

	# ALL COMMANDS ARE IMPLEMENTED HERE!

	def getParameters(self, args):
		print "=> DC Commands > Get parameters", args
		return json.dumps(self.vehicle.parameters)

	def disableArmingCheck(self, args):
		print "=> DC Commands > Disable arming check", args
		self.vehicle.parameters["ARMING_CHECK"] = 0
		return None

	def printArgs(self, args):
		print "=> DC Commands > Command runs with args =", args
		return None

	def setSpeed(self, args):
		print "=> DC Commands > set speed", args
		# Set airspeed using attribute
		self.vehicle.airspeed = args["airSpeed"] #m/s
		# Set groundspeed using attribute
		self.vehicle.groundspeed = args["groundSpeed"] #m/s
		return None

	def arm(self, args):
		print "=> DC Commands > Basic pre-arm checks", args
		# Don't let the user try to arm until autopilot is ready
		while not self.vehicle.is_armable:
			print "=> DC Commands > Waiting for vehicle to initialise..."
			time.sleep(1)

		# Copter should arm in GUIDED mode
		#self.vehicle.mode = VehicleMode("GUIDED")
		
		self.PX4setMode(4)

		print "=> DC Commands > Arming motors"
		self.vehicle.armed = True

		while not self.vehicle.armed:
			print "=> DC Commands > Waiting for arming..."
			time.sleep(1)

		return None

	def takeOff(self, args):
		print "=> DC Commands > Taking off!", args
		self.vehicle.simple_takeoff(args["z"])
		while True:
			print("=> DC Commands > Altitude: ", self.vehicle.location.global_relative_frame.alt)
			# Break and return from function just below target altitude.
			if self.vehicle.location.global_relative_frame.alt >= args["z"] * 0.95:
				print("=> DC Commands > Reached target altitude = ", args["z"])
				break
			time.sleep(1)

		return None

	def armAndTakeOff(self, args):
		self.arm(args)
		self.takeOff(args)
		return None

	def backToLand(self, args):
		print "=> DC Commands > Back to the land", args
		self.vehicle.mode = VehicleMode("LAND")
		return None

	def returnToLaunch(self, args):
		print "=> DC Commands > Return to launch", args
		self.vehicle.mode = VehicleMode("RTL")
		return None

	def rotateGimbal(self, args):
		print "=> DC Commands > Rotate gimbal", args
		self.vehicle.gimbal.rotate(args["pitch"], args["roll"], args["yaw"])
		time.sleep(2)
		return None

	def setVelocity(self, args):
		print "=> DC Commands > set velocity", args	
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
		return None

	def setPosition(self, args):
		print "=> DC Commands > set position", args
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

		return None

	def setGEOPosition(self, args):
		print "=> DC Commands > set geo position", args
		original_location = self.vehicle.location.global_frame
		if type(original_location) is LocationGlobal:
		    targetlocation=LocationGlobal(args["lat"], args["lon"], args["alt"])
		elif type(original_location) is LocationGlobalRelative:
		    targetlocation=LocationGlobalRelative(args["lat"], args["lon"], args["alt"])
		#go to new location
		self.vehicle.simple_goto(targetlocation, groundspeed=args["groundspeed"])
		return None

	def getGEOPosition(self, args):
		print "=> DC Commands > get geo position", args
		original_location = self.vehicle.location.global_frame
		return """{
			"lat": """+ original_location.lat +""",
			"lon": """+ original_location.lon +""",
			"alt": """+ original_location.alt +""",			
		}"""
	
	def initAutoMission(self, args):
		print "=> DC Commands > Create auto mission commands"
		self.autoCmds = self.vehicle.commands
		#self.autoCmds.download()
		#self.autoCmds.wait_ready() # wait until download is complete.
		print "=> DC Commands > Clear all commands"
		self.autoCmds.clear()
		print "=> DC Commands > Add MAV_CMD_NAV_TAKEOFF command. This is ignored if the vehicle is already in the air."
		self.autoCmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, args["alt"]))
		return None
		
	def addWayPointAutoMission(self, args):
		print "=> DC Commands > Add waypoint ", args
		point = LocationGlobal(args["lat"], args["lon"], args["alt"])
		self.lastAutoCmd = Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point.lat, point.lon, point.alt)
		self.autoCmds.add(self.lastAutoCmd)
		self.autoCmdsCount = self.autoCmdsCount + 1
		return None
		
	def startAutoMission(self, args):
		print "=> DC Commands > Add dummy waypoint (duplicate the last waypoint)"
		self.autoCmds.add(self.lastAutoCmd)
		
		print "=> DC Commands > Upload new commands to vehicle"
		self.autoCmds.upload()
		
		print "=> DC Commands > Reset mission set to first (0) waypoint"
		self.vehicle.commands.next = 0
		
		print "=> DC Commands > Set mode to AUTO to start mission"
		self.vehicle.mode = VehicleMode("AUTO")
		
		print "=> DC Commands > waiting vehicle complete mission"
		while True:
			nextwaypoint = self.vehicle.commands.next
			print "=> DC Commands > Next waypoint (%s)" % (nextwaypoint)
			if nextwaypoint == len(self.autoCmdsCount):
				print "=> DC Commands > End Mission"
				break;
			time.sleep(1)

		print "=> DC Commands > Return to launch"
		self.vehicle.mode = VehicleMode("RTL")
		return None

	def frameworkTests(self, args):
		threadNumber = args["threadNumber"]
		timeSend = args["timeSend"]
		timestamp = time.time() * 1000
		totalTime = timestamp - timeSend

		if self.frameworkTestsLog == None:
			self.frameworkTestsLog = logging
			now = strftime("%Y-%m-%d_%H:%M:%S", gmtime())
			self.frameworkTestsLog.basicConfig(filename='/home/pi/drone-control/drone-clients/test-framework-drone-control/logs/fw-tests-'+str(now)+'.log', filemode='w',level=logging.DEBUG)
			self.frameworkTestsLog.info("threadNumber\ttimeSend\ttimestamp\ttotalTime")

		self.frameworkTestsLog.info("%s\t%s\t%s\t%s"%(threadNumber, timeSend, timestamp, totalTime))

		return None
