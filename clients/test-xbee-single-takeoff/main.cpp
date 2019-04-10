#include <iostream>
#include <unistd.h>
#include <string>
#include <sstream>
#include "wsn-xbee.hpp"

int main(){
	
	std::cout.setf(std::ios::unitbuf);
	
	// Setup Xbee radio connection
	//WSNXbee *w = new WSNXbee("/dev/serial0", 57600);
	WSNXbee *w = new WSNXbee("/dev/ttyUSB0", 57600);
	std::cout << "Connected with the Xbee" << std::endl;
	
	std::cout << "Send message to drone 2 and takeoff 2 meters." << std::endl;
	
	int xbeeNumber = 2;
	int aTargetAltitude = 2;
	
	std::stringstream msg1;
	std::stringstream msg2;
	
	msg1 << std::fixed << "{\"drone\":" << xbeeNumber << ",\"command\":\"armAndTakeOff\",\"args\":{\"z\":" << aTargetAltitude << "}}";
	msg2 << std::fixed << "{\"drone\":" << xbeeNumber << ",\"command\":\"backToLand\",\"args\":{}}";
	
	w->send(5, msg1.str());	
	usleep(2000000);
	w->send(5, msg2.str());				
	usleep(2000000);
	
	//closing xbee connection
	w->~WSNXbee();
	
	return 0;

}
