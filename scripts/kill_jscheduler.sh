#!/bin/bash
echo "Killing JScheduler"
sudo kill $(ps aux | grep '[j]scheduler.py unique_param_for_kill_jscheduler' | awk '{print $2}')
sudo kill -9 $(ps aux | grep '[j]scheduler.py unique_param_for_kill_jscheduler' | awk '{print $2}')

if [ -n "$(ps aux | grep '[j]scheduler.py unique_param_for_kill_jscheduler')" ]
then
        echo "Not killed..."
        exit 1
fi
echo "Killing done"
# exit 0
