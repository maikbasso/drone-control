#!/user/bin/python

# @Author: Maik Basso <maik@maikbasso.com.br> 

# This script solve the problem when install dronekit
# and the "import dronekit" is not found

import pip

#install dronekit
pip.main(['install', 'dronekit'])
pip.main(['install', 'dronekit-sitl'])