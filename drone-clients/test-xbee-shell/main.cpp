#include <iostream>
#include <unistd.h>
#include <string>
#include <sstream>
#include "wsn-xbee.hpp"

int main(){
	
	std::cout.setf(std::ios::unitbuf);
	
	// Setup Xbee radio connection
	WSNXbee *w = new WSNXbee("/dev/serial0", 57600);
	std::cout << "Connected with the Xbee\n";
	
	usleep(5000000);
	
	std::cout << "Select radio: ";
	int xbeeNumber;
	std::cin >> xbeeNumber;
	
	
	int option = -1;
	
	while(option != -2){
		std::cout << "0 - arm " << std::endl;
		std::cout << "1 - setSpeed " << std::endl;
		std::cout << "2 - takeOff " << std::endl;
		std::cout << "3 - backToLand " << std::endl;
		std::cout << "4 - returnToLaunch " << std::endl;
		std::cout << "5 - rotateGimbal " << std::endl;
		std::cout << "6 - setVelocity " << std::endl;
		std::cout << "7 - setPosition " << std::endl;
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
				
				std::cout << msg.str() << std::endl;
				
				w->send(xbeeNumber, msg.str());
				break;
			case 2:
				std::cout << "z = ";
				float z;
				std::cin >> z;
				
				msg << std::fixed << "{\"command\":\"takeOff\",\"args\":{\"z\":" << z << "}}";
				
				std::cout << msg.str() << std::endl;
				
				w->send(xbeeNumber, msg.str());
				break;
			case 3:
				w->send(xbeeNumber, "{\"command\":\"backToLand\",\"args\":{}}");
				break;
			case 4:
				w->send(xbeeNumber, "{\"command\":\"returnToLaunch\",\"args\":{}}");
				break;
			case 5:
				std::cout << "pitch = ";
				float pitch;
				std::cin >> pitch;
				
				std::cout << "roll = ";
				float roll;
				std::cin >> roll;
				
				std::cout << "yaw = ";
				float yaw;
				std::cin >> yaw;
				
				msg << std::fixed << "{\"command\":\"rotateGimbal\",\"args\":{\"pitch\":" << pitch << ",\"roll\":" << roll << ",\"yaw\":" << yaw << "}}";
				
				std::cout << msg.str() << std::endl;
				
				w->send(xbeeNumber, msg.str());
				break;
			case 6:
				std::cout << "duration = ";
				float duration;
				std::cin >> duration;
				
				std::cout << "velocity_x = ";
				float velocity_x;
				std::cin >> velocity_x;
				
				std::cout << "velocity_y = ";
				float velocity_y;
				std::cin >> velocity_y;
				
				std::cout << "velocity_z = ";
				float velocity_z;
				std::cin >> velocity_z;
				
				msg << std::fixed << "{\"command\":\"setVelocity\",\"args\":{\"velocity_x\":" << velocity_x << ",\"velocity_y\":" << velocity_y << ",\"velocity_z\":" << velocity_z << ",\"duration\":" << duration << "}}";
				
				std::cout << msg.str() << std::endl;
				
				w->send(xbeeNumber, msg.str());
				break;
			case 7:
				
				std::cout << "px = ";
				float px;
				std::cin >> px;
				
				std::cout << "py = ";
				float py;
				std::cin >> py;
				
				std::cout << "pz = ";
				float pz;
				std::cin >> pz;
				
				msg << std::fixed << "{\"command\":\"setPosition\",\"args\":{\"x\":" << px << ",\"y\":" << py << ",\"z\":" << pz << "}}";
				
				std::cout << msg.str() << std::endl;
				
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
