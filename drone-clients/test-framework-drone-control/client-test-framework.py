#!/user/bin/python

# @Author: Maik Basso <maik@maikbasso.com.br> 

import socket
import time
import math
import threading

numberOfTests = 33
maxNumberOfClients = 12
sequence = 0
threads = list()

def runClient(threadNumber, numberOfTests):
	# Create a TCP/IP socket
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Connect the socket to the port where the server is listening
	client.connect(('localhost', 7000))
	# run all tasks
	for c in xrange(0, numberOfTests):
		timestamp = time.time() * 1000
		print timestamp
		client.sendall('{"command": "frameworkTests", "args": {"threadNumber": '+str(threadNumber)+',"timeSend": '+str(timestamp)+'}}')
		time.sleep(3)

#create all threads
for c in xrange(0, maxNumberOfClients):
	threadNumber = len(threads)
	threads.append(threading.Thread(target=runClient, args=(threadNumber,numberOfTests,)))
	print "Adding client number:", threadNumber

#start all threads
for t in threads:
	t.start()
	print "Starting client number"

while True:
	pass

#client.close()
#exit()