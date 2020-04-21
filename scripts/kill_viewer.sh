#!/bin/bash
echo Killing Viewers
sudo kill $(ps aux | grep '[p]ython.*viewer.py unique_param_for_kill_viewer' | awk '{print $2}')
sudo kill -9 $(ps aux | grep '[p]ython.*viewer.py unique_param_for_kill_viewer' | awk '{print $2}')

if [ -n "$(ps aux | grep '[p]ython.*viewer.py unique_param_for_kill_viewer')" ]
then
        echo "Not killed..."
        exit 1
fi
echo "Killing done"
exit 0
