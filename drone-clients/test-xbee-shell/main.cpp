#include <iostream>
#include <unistd.h>
#include <string>
#include <sstream>
#include "wsn-xbee.hpp"

int main(){
	
	std::cout.setf(std::ios::unitbuf);
	
	// Setup Xbee radio connection
	WSNXbee *w = new WSNXbee("/dev/serial0", 57600);
	usleep(5000000);
	std::cout << "Connected with the Xbee\n";
	
	std::cout << "Select radio: ";
	int xbeeNumber;
	std::cin >> xbeeNumber;
	
	int option = -1;
	
	while(option != -2){
		std::cout << "0 - arm " << std::endl;
		std::cout << "1 - setSpeed " << std::endl;
		std::cout << "Select an option > ";
		std::cin >> option;
		
		std::stringstream msg;
		
		switch(option){
			case 0:
				w->send(xbeeNumber, "{\"command\":\"arm\",\"args\":{}}");
				break;
			case 1:
				std::cout << "groundSpeed = ";
				float groundSpeed;
				std::cin >> groundSpeed;
				
				std::cout << "airSpeed = ";
				float airSpeed;
				std::cin >> airSpeed;
				
				msg << std::fixed << "{\"command\":\"setSpeed\",\"args\":{\"airSpeed\":" << airSpeed << ",\"groundSpeed\":" << groundSpeed << "}}";
				
				w->send(xbeeNumber, msg.str());
				break;
			default:
				option = -2;
				break;
		}
		
		usleep(1000000);
	
	}
	
	//closing xbee connection
	w->~WSNXbee();
	
	return 0;

}
