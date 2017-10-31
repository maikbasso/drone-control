#!/bin/bash

# @Author: Maik Basso <maik@maikbasso.com.br>

# install linux dependencies
sudo apt-get install -y python-pip python-dev python-numpy python-opencv python-serial python-pyparsing python-wxgtk2.8

# install python dependencies
sudo -H python install-python-dependencies.py

# add current user in dialout group
sudo adduser $USER dialout
