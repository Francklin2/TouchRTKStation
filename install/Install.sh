#!/bin/sh

cd /home/pi/

apt-get update -y

# Install pyqt5
apt-get install -y qt5-default pyqt5-dev pyqt5-dev-tools

# Install RTKLIB
git clone -b rtklib_2.4.3 https://github.com/tomojitakasu/RTKLIB.git
cd ./RTKLIB/app/str2str/gcc/
make
cd ../../rtkrcv/gcc/
make

# Install LCD Driver
cd /home/pi/
git clone https://github.com/waveshare/LCD-show.git
cd ./LCD-show/
chmod +x LCD5-show
./LCD5-show
