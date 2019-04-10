#include <iostream>
#include <fstream>
#include <unistd.h>
#include "client.hpp"
#include "wsn-xbee.hpp"
#include "json.hpp"
#include <vector>
#include <chrono>

int main(){
	std::cout.setf(std::ios::unitbuf);
	//list of xbee
	std::vector<int> xbeeList = {5};
    
    //results file id
    time_t rawtime;
    struct tm * timeinfo;
    char buffer[80];
    time (&rawtime);
    timeinfo = localtime(&rawtime);
    strftime(buffer,sizeof(buffer),"/home/pi/drone-control/drone-clients/test-xbee-control/log/test_%d-%m-%Y_%H-%M-%S.txt",timeinfo);
    string resultsFileId(buffer);

    //results file
    ofstream resultsFile;
    resultsFile.open(resultsFileId);
	
	// Setup Flight Controller connection	
	TCPClient *c = new TCPClient();
	c->conn("localhost",7000);
	resultsFile << "Connected with the Flight Controller\n";
	resultsFile.flush();

	// Setup Xbee radio connection
	WSNXbee *w = new WSNXbee("/dev/serial0", 57600);
	resultsFile << "Connected with the Xbee\n";
	resultsFile.flush();
	
    
	// Waiting for commands
	for(;;){
		
		for(int i = 0; i < xbeeList.size(); i++){
			std::string data;
			
			//receive data
			w->receive(xbeeList.at(i), data);
			
			
			// if data isn't empty
			if (!data.empty()) {
				
				using json = nlohmann::json;
				auto j3 = json::parse(data);
				int drone = j3["drone"];
				if(drone == 1){
					// send command to the flight controller
					c->sendData(data);
				}
				else if(drone == 99){
					long timestamp = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::time_point_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now()).time_since_epoch()).count();
					resultsFile << data << "\t" << timestamp << "\n";
					resultsFile.flush();
				}
				else{
					// writing log
					resultsFile << data << "\n";
					resultsFile.flush();
				}
				
			}
						
        }
        
        //one in one second
		usleep(1000000);
	}
	
	//closing xbee connection
	w->~WSNXbee();
	resultsFile << "closing xbee connection\n";
    resultsFile.flush();
	
	//close the results file
	resultsFile << "closing log\n";
    resultsFile.flush();
    resultsFile.close();
	
	return 0;

}
