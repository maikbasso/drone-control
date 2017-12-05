#include <iostream>
#include <fstream>
#include <unistd.h>
#include "client.hpp"
#include "wsn-xbee.hpp"
#include "json.hpp"
#include <vector>

int main(){
	//list of xbee
	std::vector<int> xbeeList = {1};
    
    //results file id
    time_t rawtime;
    struct tm * timeinfo;
    char buffer[80];
    time (&rawtime);
    timeinfo = localtime(&rawtime);
    strftime(buffer,sizeof(buffer),"log/test_%d-%m-%Y_%H-%M-%S.txt",timeinfo);
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
		
		for(int i; i <= xbeeList.size(); i++){
			std::string data;
			
			//receive data
			w->receive(xbeeList.at(i), data);
			
			// if data isn't empty
			if (!data.empty()) {
				
				// send command to the flight controller
				c->sendData(data);
				
				// writing log
				resultsFile << data << "\n";
				resultsFile.flush();
				
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
