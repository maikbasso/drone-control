#!/bin/bash

# @Author: Maik Basso <maik@maikbasso.com.br>

# update your operating system
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y
sudo rpi-update -y

# install linux dependencies
sudo apt-get install -y python-pip python-dev python-numpy python-opencv python-serial python-pyparsing python-wxgtk2.8

#install pymavlink
sudo pip2 install -U pymavlink

# add current user in dialout group
sudo adduser $USER dialout

# install dronekit
cd ~
git clone https://github.com/dronekit/dronekit-python.git
cd ./dronekit-python
sudo python setup.py build
sudo python setup.py install

# go to drone-control folder
cd ~/drone-control

# initialize submodules:
git submodule init
git submodule update

# go to drone-control scripts folder
cd ./scripts