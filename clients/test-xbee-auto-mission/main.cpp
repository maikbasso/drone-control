#include <iostream>
#include <unistd.h>
#include <string>
#include <sstream>
#include "wsn-xbee.hpp"
#include <chrono>

int main(){
	
	std::cout.setf(std::ios::unitbuf);
	
	// Setup Xbee radio connection
	//WSNXbee *w = new WSNXbee("/dev/serial0", 57600);
	WSNXbee *w = new WSNXbee("/dev/ttyUSB0", 57600);
	std::cout << "Connected with the Xbee" << std::endl;
	
	int xbeeNumber = 1;
	
	std::stringstream msg1;
	std::stringstream msg2;
	std::stringstream msg3;
	std::stringstream msg4;
	
	
	msg1 << std::fixed << "{\"drone\":" << xbeeNumber << ",\"command\":\"initAutoMission\",\"args\":{\"alt\": 10}}";

	msg2 << std::fixed << "{\"drone\":" << xbeeNumber << ",\"command\":\"addWayPointAutoMission\",\"args\":{\"lat\": -30.076462,\"lon\": -51.118124,\"alt\": 10}}";

	msg3 << std::fixed << "{\"drone\":" << xbeeNumber << ",\"command\":\"addWayPointAutoMission\",\"args\":{\"lat\": -30.076449,\"lon\": -51.117063,\"alt\": 10}}";

	msg4 << std::fixed << "{\"drone\":" << xbeeNumber << ",\"command\":\"startAutoMission\",\"args\":{}}";

	w->send(5, msg1.str());	
	usleep(2000000);
	w->send(5, msg2.str());	
	usleep(2000000);
	w->send(5, msg3.str());	
	usleep(2000000);
	w->send(5, msg4.str());				
	usleep(2000000);
	
	while(true){
		std::stringstream msg;
		long timestamp = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::time_point_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now()).time_since_epoch()).count();
		msg << std::fixed << "{\"drone\": 99, \"command\":\"timestamp\",\"args\":{\"timestamp\": "<< timestamp << "}}";
		w->send(5, msg.str());
		usleep(500000);	
	}
	
	//closing xbee connection
	w->~WSNXbee();
	
	return 0;

}
