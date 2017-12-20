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
        std::cout << " 0 - disableArmingCheck " << std::endl;
		std::cout << " 1 - arm " << std::endl;
		std::cout << " 2 - setSpeed " << std::endl;
		std::cout << " 3 - takeOff " << std::endl;
		std::cout << " 4 - armAndTakeOff " << std::endl;
		std::cout << " 5 - backToLand " << std::endl;
		std::cout << " 6 - returnToLaunch " << std::endl;
		std::cout << " 7 - rotateGimbal " << std::endl;
		std::cout << " 8 - setVelocity " << std::endl;
		std::cout << " 9 - setPosition " << std::endl;
		std::cout << "10 - setGEOPosition " << std::endl;
		std::cout << "11 - getGEOPosition " << std::endl;
		std::cout << "12 - square_MissionVale (Caution!!! You should only run on the Campus of Vale.)" << std::endl;
		std::cout << "13 - spy_MissionVale (Caution!!! You should only run on the Campus of Vale.) " << std::endl;		
		std::cout << "Select an option > ";
		std::cin >> option;
		
		std::stringstream msg;
		
		switch(option){
			case 0:
				msg << std::fixed << "{\"drone\":" << xbeeNumber << ",\"command\":\"disableArmingCheck\",\"args\":{}}";
				std::cout << msg.str() << std::endl;
				w->send(5, msg.str());
				break;
			case 1:
				msg << std::fixed << "{\"drone\":" << xbeeNumber << ",\"command\":\"arm\",\"args\":{}}";
				std::cout << msg.str() << std::endl;
				w->send(5, msg.str());
				break;
			case 2:
				std::cout << "groundSpeed = ";
				float groundSpeed;
				std::cin >> groundSpeed;
				
				std::cout << "airSpeed = ";
				float airSpeed;
				std::cin >> airSpeed;
				
				msg << std::fixed << "{\"drone\":" << xbeeNumber << ",\"command\":\"setSpeed\",\"args\":{\"airSpeed\":" << airSpeed << ",\"groundSpeed\":" << groundSpeed << "}}";
				std::cout << msg.str() << std::endl;
				w->send(5, msg.str());
				break;
			case 3:
				std::cout << "Target altitude = ";
				float z;
				std::cin >> z;
				
				msg << std::fixed << "{\"drone\":" << xbeeNumber << ",\"command\":\"takeOff\",\"args\":{\"z\":" << z << "}}";
				std::cout << msg.str() << std::endl;
				w->send(5, msg.str());
				break;
			case 4:
								
				std::cout << "Target altitude = ";
				int aTargetAltitude;
				std::cin >> aTargetAltitude;
				
				msg << std::fixed << "{\"drone\":" << xbeeNumber << ",\"command\":\"armAndTakeOff\",\"args\":{\"z\":" << aTargetAltitude << "}}";
				std::cout << msg.str() << std::endl;
				w->send(5, msg.str());
				break;
			case 5:
				msg << std::fixed << "{\"drone\":" << xbeeNumber << ",\"command\":\"backToLand\",\"args\":{}}";
				std::cout << msg.str() << std::endl;
				w->send(5, msg.str());
				break;
			case 6:
				msg << std::fixed << "{\"drone\":" << xbeeNumber << ",\"command\":\"returnToLaunch\",\"args\":{}}";
				std::cout << msg.str() << std::endl;
				w->send(5, msg.str());
				break;
			case 7:
				std::cout << "pitch = ";
				float pitch;
				std::cin >> pitch;
				
				std::cout << "roll = ";
				float roll;
				std::cin >> roll;
				
				std::cout << "yaw = ";
				float yaw;
				std::cin >> yaw;
				
				msg << std::fixed << "{\"drone\":" << xbeeNumber << ",\"command\":\"rotateGimbal\",\"args\":{\"pitch\":" << pitch << ",\"roll\":" << roll << ",\"yaw\":" << yaw << "}}";
				std::cout << msg.str() << std::endl;
				w->send(5, msg.str());
				break;
			case 8:
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
				
				msg << std::fixed << "{\"drone\":" << xbeeNumber << ",\"command\":\"setVelocity\",\"args\":{\"velocity_x\":" << velocity_x << ",\"velocity_y\":" << velocity_y << ",\"velocity_z\":" << velocity_z << ",\"duration\":" << duration << "}}";
				std::cout << msg.str() << std::endl;
				w->send(5, msg.str());
				break;
			case 9:
				
				std::cout << "px = ";
				float px;
				std::cin >> px;
				
				std::cout << "py = ";
				float py;
				std::cin >> py;
				
				std::cout << "pz = ";
				float pz;
				std::cin >> pz;
				
				msg << std::fixed << "{\"drone\":" << xbeeNumber << ",\"command\":\"setPosition\",\"args\":{\"x\":" << px << ",\"y\":" << py << ",\"z\":" << pz << "}}";
				std::cout << msg.str() << std::endl;
				w->send(5, msg.str());
				break;
			case 10:
				std::cout << "latitude = ";
				float lat;
				std::cin >> lat;
				
				std::cout << "Longitude = ";
				float lon;
				std::cin >> lon;
				
				std::cout << "Altitude = ";
				float alt;
				std::cin >> alt;
				
				std::cout << "Ground Speed = ";
				std::cin >> groundSpeed;

				msg << std::fixed << "{\"drone\":" << xbeeNumber << ",\"command\":\"setGEOPosition\",\"args\":{\"lat\":" << lat << ",\"lon\":" << lon << ",\"alt\":" << alt << ",\"groundSpeed\":" << groundSpeed << "}}";
				std::cout << msg.str() << std::endl;
				w->send(5, msg.str());
				break;
			case 11:
				msg << std::fixed << "{\"drone\":" << xbeeNumber << ",\"command\":\"getGEOPosition\",\"args\":{}}";
				std::cout << msg.str() << std::endl;
				w->send(5, msg.str());
				
				for(;;){
					std::string data;
					
					//receive data
					w->receive(5, data);
					
					// if data isn't empty
					if (!data.empty()) {
						
						std::cout << "GEO POSITION response = " << data << std::endl;
						break;
						
					}
					
					//one in one second
					usleep(1000000);
				}
				
				break;
			case 12:
				msg << std::fixed << "{\"drone\":" << xbeeNumber << ",\"command\":\"squareMissionVale\",\"args\":{}}";
				std::cout << msg.str() << std::endl;
				w->send(5, msg.str());
				break;
			case 13:
				msg << std::fixed << "{\"drone\":" << xbeeNumber << ",\"command\":\"spyMissionVale\",\"args\":{}}";
				std::cout << msg.str() << std::endl;
				w->send(5, msg.str());
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
