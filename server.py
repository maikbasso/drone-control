#!/user/bin/python

# @Author: Maik Basso <maik@maikbasso.com.br>

# import DroneControl lib
from lib.dronecontrol import DroneControl

#connect to vehicle
drone = DroneControl("udpin:0.0.0.0:14550", "localhost", 7000, 12)
#drone = DroneControl("/dev/ttyACM0", 57600, "localhost", 7000, 12)
#drone = DroneControl("/dev/ttyAMA0", 57600, "localhost", 7000, 12)
#drone = DroneControl("/dev/ttyS0", 57600, "localhost", 7000, 12)
#drone = DroneControl("/dev/serial0", 57600, "localhost", 7000, 12)


# auto startup clients [OPCIONAL]
#drone.registerClient("python ../clients/test-circle/client-test-circle.py")
#drone.registerClient("python ../clients/test-shell/client-test-shell.py")
#drone.registerClient("python ../clients/test-square/client-test-square.py")
#drone.registerClient("python ../clients/test-virtual-joystick/client-test-virtual-joystick.py")
#drone.registerClient("./../clients/test-plant-line-detection/build/main")
#drone.registerClient("./../clients/test-xbee-control/main")
#drone.registerClient("./../clients/test-xbee-shell/main")
#drone.registerClient("./../clients/test-xbee-single-takeoff/main")
#drone.registerClient("python ../clients/test-auto-mission/client-test-auto-mission.py")
drone.registerClient("python ../clients/test-simple-takeoff/client-test-simple-takeoff.py")

#start clients
drone.startClients()
