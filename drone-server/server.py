#!/user/bin/python

# @Author: Maik Basso <maik@maikbasso.com.br>

# define library folder
import sys
sys.path.append("../drone-lib")

# import DroneControl lib
from dronecontrol import DroneControl

#connect to vehicle
#drone = DroneControl("udpin:0.0.0.0:14550", 57600, "localhost", 7000, 12)
drone = DroneControl("/dev/ttyACM0", 57600, "localhost", 7000, 12)
#drone = DroneControl("/dev/ttyAMA0", 57600, "localhost", 7000, 12)
#drone = DroneControl("/dev/ttyS0", 57600, "localhost", 7000, 12)
#drone = DroneControl("/dev/serial0", 57600, "localhost", 7000, 12)


# auto startup clients [OPCIONAL]
#drone.registerClient("python ../drone-clients/test-circle/client-test-circle.py")
#drone.registerClient("python ../drone-clients/test-shell/client-test-shell.py")
#drone.registerClient("python ../drone-clients/test-square/client-test-square.py")
#drone.registerClient("python ../drone-clients/test-virtual-joystick/client-test-virtual-joystick.py")
#drone.registerClient("./../drone-clients/test-plant-line-detection/build/main")
#drone.registerClient("./../drone-clients/test-xbee-control/main")
#drone.registerClient("./../drone-clients/test-xbee-shell/main")
#drone.registerClient("./../drone-clients/test-xbee-single-takeoff/main")
#drone.registerClient("python ../drone-clients/test-auto-mission/client-test-auto-mission.py")
drone.registerClient("python ../drone-clients/test-simple-takeoff/client-test-simple-takeoff.py")

#start clients
drone.startClients()
