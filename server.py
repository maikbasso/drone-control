#!/user/bin/python

# @Author: Maik Basso <maik@maikbasso.com.br>

# import DroneControl lib
from lib.dronecontrol import DroneControl
import subprocess
import os
import time


####################### colocar isso num arquivo separado ##########################################
# Inicializa o Gazebo
# os.system("sudo killall -9 gazebo")
# os.system("sudo killall -9 gzserver")
# os.system("sudo killall -9 gzclient")
print("********************  ok0  ********************")


processG = subprocess.Popen("gazebo --verbose /usr/share/gazebo-8/worlds/simulacao_multivant.world", shell=True, stdout=subprocess.PIPE)
print("********************  ok Gazebo  ********************")

process1 = subprocess.Popen("python /home/lucasgrazziotim/ardupilot/Tools/autotest/sim_vehicle.py -v ArduCopter -f gazebo-iris  -I0", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#process2 = subprocess.Popen("python sim_vehicle.py -v ArduCopter -f gazebo-iris  -I1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print("********************  ok process  ********************")

time.sleep(10)
####################################################################################################


#connect to vehicle
drone = DroneControl(
	droneHost = "udpin:0.0.0.0:14550",
	socketHost = "localhost",
	socketPort = 7000,
	socketMaxClients = 12
)
#drone = DroneControl("/dev/ttyACM0", 57600, "localhost", 7000, 12)
#drone = DroneControl("/dev/ttyAMA0", 57600, "localhost", 7000, 12)
#drone = DroneControl("/dev/ttyS0", 57600, "localhost", 7000, 12)
#drone = DroneControl("/dev/serial0", 57600, "localhost", 7000, 12)


# auto startup clients [OPCIONAL]
drone.registerClient("python ./clients/test-Lucas/client-square.py")
#drone.registerClient("python ./clients/test-shell/client-test-shell.py")
#drone.registerClient("python ./clients/test-square/client-test-square.py")
#drone.registerClient("python ../clients/test-virtual-joystick/client-test-virtual-joystick.py")
#drone.registerClient("./clients/test-plant-line-detection/build/main")
#drone.registerClient("./clients/test-xbee-control/main")
#drone.registerClient("./clients/test-xbee-shell/main")
#drone.registerClient("./clients/test-xbee-single-takeoff/main")
#drone.registerClient("python ./clients/test-auto-mission/client-test-auto-mission.py")
#drone.registerClient("python ./clients/test-simple-takeoff/client-test-simple-takeoff.py")

#start clients
drone.startClients()
