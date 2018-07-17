#!/bin/bash

# @Author: Maik Basso <maik@maikbasso.com.br>

# update your operating system
echo "Updating OS and Raspberry Pi Firmware"
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y
sudo rpi-update -y

echo "Installing all dependencies"
# install linux dependencies
sudo apt-get install -y python-pip python-dev python-numpy python-opencv python-serial python-pyparsing python-wxgtk2.8
#install pymavlink
sudo pip2 install -U pymavlink

# add current user in dialout group
echo "Enabling access to serial communication"
sudo adduser $USER dialout

# install dronekit
echo "Installing dronekit"
cd ~
git clone https://github.com/dronekit/dronekit-python.git
cd ./dronekit-python
sudo python setup.py build
sudo python setup.py install

echo "Installing framework submodules"
# go to drone-control folder
cd ~/drone-control
# initialize submodules:
git submodule init
git submodule update

echo "Installation Complete."

# update flight control firmware
echo "* Please keep the firmware of your flight control updated."
echo "* Please keep the drone sensors calibrated."