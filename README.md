# Drone-Control
Autonomous mission control framework for single or multiple UAV.

## Install on Raspberry PI using the Raspbian OS
Clone Drone-Control repository at home folder:
```
$ cd ~ && git clone https://github.com/maikbasso/drone-control.git
```
Install Drone-Control with all dependencies:
```
$ sh ~/drone-control/scripts/install-drone-control.sh
```

## Configure the server
Edit the `server.py` file to compose your system structure. Configure the connection to your flight control.
```
$ nano ~/drone-control/drone-server/server.py
```

## Starting drone server
Use the following command to start the server:
```
$ sh ~/drone-control/scripts/start-drone-server.sh
```

## Start the clients manually [optional]
For example, start the `client-shell` using this command:
```
$ python ~/drone-control/drone-clients/test-shell/client-test-shell.py
```

## Implement your commands
Edit the `dccommands.py` file to implement your functions.
```
$ nano ~/drone-control/drone-lib/dccommands.py
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