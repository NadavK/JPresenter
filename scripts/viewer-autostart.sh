#!/bin/bash

cd /home/pi/Documents/jpresenter
echo $(pwd)
echo $(whoami)

scripts/kill_viewer.sh
#if [ $? -ne 0 ]
#then
#  echo "Rebooting..."
#  echo "$USER"
#  echo sudo "$USER"
#  #sudo reboot
#  #exit
#fi

echo Changing Directory
cd /home/pi/Documents/jpresenter
pwd

echo Loading Virtual Wrapper
source env/bin/activate

echo Starting Viewer
exec /usr/local/bin/python3.6 viewer.py unique_param_for_kill_viewer > log/viewer.out

# WATCHDOG
#modprobe bcm2708_wdog
#export INFOBEAMER_WATCHDOG=30
