#!/user/bin/python

# @Author: Maik Basso <maik@maikbasso.com.br>

# define library folder
import sys
sys.path.append("../drone-lib")

# import DroneControl lib
from dronecontrol import DroneControl

#connect to simulator (vehicleHost, vehicleBaudRate, serverHost, serverPort, serverMaxClients)
drone = DroneControl("tcp:127.0.0.1:5760", 57600, "localhost", 7000, 12)

#connect to vehicle
#drone = DroneControl("/dev/ttyACM0", 57600, "localhost", 7000, 12)

# auto startup clients [OPCIONAL]
#drone.registerClient("python ../drone-clients/test-circle/client-test-circle.py")
#drone.registerClient("python ../drone-clients/test-shell/client-test-shell.py")
#drone.registerClient("python ../drone-clients/test-square/client-test-square.py")
#drone.registerClient("python ../drone-clients/test-virtual-joystick/client-test-virtual-joystick.py")
#drone.registerClient("./../drone-clients/test-plant-line-detection/build/main")

#start clients
drone.startClients()
