# drone-control
Autonomous mission control for single or multiple UAV.

## Install on Raspberry PI using the Raspbian OS
At the terminal, access the home folder:
```
$ cd ~
```
Clone repository:
```
$ git clone https://github.com/maikbasso/drone-control.git
```
Access the project folder:
```
$ cd drone-control
```
Initialize submodules:
```
$ git submodule init
$ git submodule update
```
Install all dependencies (enter your password if necessary):
```
$ cd install && sh install.sh && cd ..
```

## Mount the server
Edit the `server.py` file to compose your system structure. Configure the connection to simulator or the vehicle.
```
$ nano drone-server/server.py
```

## Starting simulator [optional]
Use the following command to start the simulator:
```
$ cd startup/ && sh start-simulator.sh
```

## Starting drone server
Use the following command to start the server:
```
$ cd startup/ && sh start-drone-server.sh
```

## Start ground station [optional]
Use this command to start ground station:
```
$ ./ground-station/QGroundControl.AppImage
```
In QGroundControl, configure the connection to the TCP host `127.0.0.1` and port `5762`. Use the baud rate of `57600`.

## Start the clients manually [optional]
For example, start the `client-shell` using this command:
```
$ python drone-clients/test-shell/client-test-shell.py
```

## Implement your commands
Edit the `dccommands.py` file to implement your functions.
```
$ nano drone-lib/dccommands.py
```
Each command is represented by a function in class `DCCommands`. Each command can be exchanged between client and server. A command is a JSON object with basically two items. The first `command` represents the name of the command to execute and the second item is` args` which is an array of parameters for the function.
An example command can be seen below:
```
{
    "command": "setPosition",
    "args": {
        "x": 10,
        "y": 5,
        "z": 2,
    }
}
```
A function in drone server receive these commands and decodes the JSON object, then executes the function indicated in the command and pass the array of arguments by parameter.