#!/bin/bash

cd /home/pi/Documents/jpresenter
echo $(pwd)
echo $(whoami)

scripts/kill_jscheduler.sh
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

echo Starting JScheduler
python3 jscheduler.py unique_param_for_kill_jscheduler > log/jscheduler.out
