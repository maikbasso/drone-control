#!/user/bin/python

# @Author: Maik Basso <maik@maikbasso.com.br>

import numpy as np
import cv2
import socket

# Create a TCP/IP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
client.connect(('localhost', 7000))

def nothing(x):
    pass

cv2.namedWindow('mask')

# create trackbars for color change
cv2.createTrackbar('H_MIN','mask',0,255,nothing)
cv2.createTrackbar('H_MAX','mask',0,255,nothing)
cv2.createTrackbar('S_MIN','mask',0,255,nothing)
cv2.createTrackbar('S_MAX','mask',0,255,nothing)
cv2.createTrackbar('V_MIN','mask',0,255,nothing)
cv2.createTrackbar('V_MAX','mask',0,255,nothing)

cv2.setTrackbarPos('H_MIN','mask',56)
cv2.setTrackbarPos('H_MAX','mask',95)
cv2.setTrackbarPos('S_MIN','mask',48)
cv2.setTrackbarPos('S_MAX','mask',255)
cv2.setTrackbarPos('V_MIN','mask',14)
cv2.setTrackbarPos('V_MAX','mask',255)

buttons = {
	0: {"x1": 10,	"y1": 10, 	"x2": 60, 	"y2": 60,	"name":"ARM"},
	1: {"x1": 70, 	"y1": 10, 	"x2": 120, 	"y2": 60, 	"name":"TKOFF"},
	2: {"x1": 130, 	"y1": 10, 	"x2": 180, 	"y2": 60, 	"name":"LAND"},
	3: {"x1": 580, 	"y1": 10, 	"x2": 630, 	"y2": 60, 	"name":"G_UP"},
	4: {"x1": 580, 	"y1": 70, 	"x2": 630, 	"y2": 120, 	"name":"G_DOWN"},
	5: {"x1": 10, 	"y1": 320, 	"x2": 60, 	"y2": 390, 	"name":"UP"},
	6: {"x1": 10, 	"y1": 400, 	"x2": 60, 	"y2": 470, 	"name":"DOWN"},
	7: {"x1": 520, 	"y1": 314, 	"x2": 570, 	"y2": 364, 	"name":"Y+"},
	8: {"x1": 460, 	"y1": 370, 	"x2": 510, 	"y2": 420, 	"name":"X-"},
	9: {"x1": 580, 	"y1": 365, 	"x2": 630, 	"y2": 420, 	"name":"X+"},
	10: {"x1": 520, "y1": 420, 	"x2": 570, 	"y2": 470, 	"name":"Y-"},
	11: {"x1": 190, "y1": 10, 	"x2": 240, 	"y2": 60, 	"name":"SPEED"}
}

cap = cv2.VideoCapture(0)

args = {
	"x":0,
	"y":0,
	"z":0,
	"gP":0,
	"gR":0,
	"gY":0,
}

buttonPressed = {"name":""}
lastCommand = ""

while(True):
	#capture frame
	ret, frame = cap.read()
	#flip frame
	frame = cv2.flip( frame, 1 )
	#convert to hsv
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	#get color thresholds
	greenLower = (
		cv2.getTrackbarPos('H_MIN','mask'),
		cv2.getTrackbarPos('S_MIN','mask'),
		cv2.getTrackbarPos('V_MIN','mask')
	)
	greenUpper = (
		cv2.getTrackbarPos('H_MAX','mask'),
		cv2.getTrackbarPos('S_MAX','mask'),
		cv2.getTrackbarPos('V_MAX','mask')
	)
	#create the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	cv2.imshow('mask', mask)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	X = -1
	Y = -1
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		if radius > 5:
			X = int(x)
			Y = int(y)
			# draw the circle and centroid on the frame
			cv2.circle(frame, (X, Y), int(radius), (0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
	
	count = len(buttons)
	#draw the options on the frame
	for i in buttons:
		button = buttons[i]
		cv2.rectangle(frame, (button["x1"], button["y1"]), (button["x2"], button["y2"]), (255,0,0), 2)
		cv2.putText(frame,button["name"],(button["x1"]+5,button["y1"]+25), cv2.FONT_HERSHEY_PLAIN , 0.7, (255,255,255), 1, cv2.LINE_AA)
		if(button["x1"] <= X <= button["x2"]) and (button["y1"] <= Y <= button["y2"]):
			buttonPressed = button
			cv2.rectangle(frame, (buttonPressed["x1"], buttonPressed["y1"]), (buttonPressed["x2"], buttonPressed["y2"]), (0,255,0), 2)
			count = count - 1

	if count == len(buttons):
		buttonPressed = {"name":""}
		lastCommand = ""

	if buttonPressed["name"] != lastCommand:
		print "button pressed=", buttonPressed["name"]
		lastCommand = buttonPressed["name"]
		message = None
		if buttonPressed["name"] == "ARM":
			message = '{"command": "arm", "args": {}}'
		if buttonPressed["name"] == "TKOFF":
			args["z"] = 2
			message = '{"command": "takeOff", "args": {"z": %d}}'%(args["z"])
		if buttonPressed["name"] == "SPEED":
			message = '{"command": "setSpeed", "args": {"airSpeed": 7,"groundSpeed": 5}}'
		if buttonPressed["name"] == "LAND":
			message = '{"command": "backToLand", "args": {}}'
		if buttonPressed["name"] == "G_UP":
			args["gP"] = args["gP"] + 10
			message = '{"command": "rotateGimbal", "args": {"pitch":%d,"roll":0,"yaw":0}}'%(args["gP"])
		if buttonPressed["name"] == "G_DOWN":
			args["gP"] = args["gP"] - 10
			message = '{"command": "rotateGimbal", "args": {"pitch":%d,"roll":0,"yaw":0}}'%(args["gP"])
		if buttonPressed["name"] == "UP":
			args["x"] = 0
			args["y"] = 0
			args["z"] = 2
			message = '{"command": "setPosition", "args": {"x": %d,"y": %d,"z":%d}}'%(args["x"],args["y"],args["z"])
		if buttonPressed["name"] == "DOWN":
			args["x"] = 0
			args["y"] = 0
			args["z"] = -2
			message = '{"command": "setPosition", "args": {"x": %d,"y": %d,"z":%d}}'%(args["x"],args["y"],args["z"])
		if buttonPressed["name"] == "Y+":
			args["x"] = 0
			args["y"] = 5
			args["z"] = 0
			message = '{"command": "setPosition", "args": {"x": %d,"y": %d,"z":%d}}'%(args["x"],args["y"],args["z"])
		if buttonPressed["name"] == "Y-":
			args["x"] = 0
			args["y"] = -5
			args["z"] = 0
			message = '{"command": "setPosition", "args": {"x": %d,"y": %d,"z":%d}}'%(args["x"],args["y"],args["z"])
		if buttonPressed["name"] == "X+":
			args["x"] = 5
			args["y"] = 0
			args["z"] = 0
			message = '{"command": "setPosition", "args": {"x": %d,"y": %d,"z":%d}}'%(args["x"],args["y"],args["z"])
		if buttonPressed["name"] == "X-":
			args["x"] = -5
			args["y"] = 0
			args["z"] = 0
			message = '{"command": "setPosition", "args": {"x": %d,"y": %d,"z":%d}}'%(args["x"],args["y"],args["z"])

		#send message
		client.sendall(message)
		
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# cleanup the camera
cap.release()
client.close()