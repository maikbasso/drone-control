#include <iostream>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <xbee.h>
#include <string>
#include <sstream>

class WSNXbee{
  public:
    WSNXbee(std::string port, int baudrate);
    ~WSNXbee();
    void send(int numberOfXbee, std::string data);
    void receive(int numberOfXbee, std::string& data);

 private:
	struct xbee_conAddress address;
    struct xbee *xbee;
	struct xbee_con *con;
	void selectRadio(int n);
	int actualRadio;
};

// constructor
WSNXbee::WSNXbee(std::string port_, int baudrate){
	this->actualRadio = -1;
	xbee_setup(&this->xbee, "xbeeZB", port_.c_str(), baudrate);
}

// destructor
WSNXbee::~WSNXbee(){
	/* close the connection */
	xbee_conEnd(this->con);

	/* shutdown libxbee */
	xbee_shutdown(this->xbee);
}

void WSNXbee::selectRadio(int n){

	if(this->actualRadio != n){
		/* close the connection */
		xbee_conEnd(this->con);

		int status = 0;

		if(n == 1){
			memset(&this->address, 0, sizeof(this->address));
			this->address.addr64_enabled = 1;
			this->address.addr64[0] = 0x00;
			this->address.addr64[1] = 0x13;
			this->address.addr64[2] = 0xA2;
			this->address.addr64[3] = 0x00;
			this->address.addr64[4] = 0x40;
			this->address.addr64[5] = 0xAE;
			this->address.addr64[6] = 0x9B;
			this->address.addr64[7] = 0xFE;
			status = 1;
			this->actualRadio = n;
		}
		else if(n == 2){
			memset(&this->address, 0, sizeof(this->address));
			this->address.addr64_enabled = 1;
			this->address.addr64[0] = 0x00;
			this->address.addr64[1] = 0x13;
			this->address.addr64[2] = 0xA2;
			this->address.addr64[3] = 0x00;
			this->address.addr64[4] = 0x40;
			this->address.addr64[5] = 0xAC;
			this->address.addr64[6] = 0xC3;
			this->address.addr64[7] = 0x10;
			status = 1;
			this->actualRadio = n;
		}
		else if(n == 3){
			memset(&this->address, 0, sizeof(this->address));
			this->address.addr64_enabled = 1;
			this->address.addr64[0] = 0x00;
			this->address.addr64[1] = 0x13;
			this->address.addr64[2] = 0xA2;
			this->address.addr64[3] = 0x00;
			this->address.addr64[4] = 0x40;
			this->address.addr64[5] = 0xAE;
			this->address.addr64[6] = 0x9C;
			this->address.addr64[7] = 0xB0;
			status = 1;
			this->actualRadio = n;
		}
		else if(n == 4){
			memset(&this->address, 0, sizeof(this->address));
			this->address.addr64_enabled = 1;
			this->address.addr64[0] = 0x00;
			this->address.addr64[1] = 0x00;
			this->address.addr64[2] = 0x00;
			this->address.addr64[3] = 0x00;
			this->address.addr64[4] = 0x00;
			this->address.addr64[5] = 0x00;
			this->address.addr64[6] = 0xFF;
			this->address.addr64[7] = 0xFF;
			status = 1;
			this->actualRadio = n;
		}
		else{
			std::cout << "Xbee not found!\n";
			return;
		}

		if(status == 1){

			/* create a 64-bit data connection with the address */
			xbee_conNew(xbee, &this->con, "Data", &this->address);

		}
		else{
			this->selectRadio(1);
		}
	}

}

void WSNXbee::send(int numberOfXbee, std::string message){

	this->selectRadio(numberOfXbee);

	//send data
	xbee_conTx(this->con, NULL, message.c_str());
}

void WSNXbee::receive(int numberOfXbee, std::string& data){

		this->selectRadio(numberOfXbee);

		struct xbee_pkt *pkt;

		//xbee_conTx(con, NULL, "HelloTest");

		usleep(100000);

		if (xbee_conRx(this->con, &pkt, NULL) != XBEE_ENONE) {

			data = std::string();
            return;

        }

        //xbee_conRx(this->con, &pkt, NULL);

        //convert char array to string
        std::stringstream ss;
        ss << pkt->data;

		data = ss.str();
        return;
}
