# JPresenter
Displays full-screen images, for digital picture frames using Raspberry Pi.<br>
Images are selected from directories, taking into account the Jewish holidays: Images from the Shabbat directory are displayed on Shabbat, the Pesach directory on Pesach... you get the idea.<br>
Images change every 30 minutes, on the half-hour.

## Overview
```jscheduler``` writes to the ```playlist``` file the name of the current Jewish holiday, and the day 'part': ```Evening```, ```Morning```, ```Afternoon```, and ```Motzei```.   
```viewer.py``` refers to the listings in the ```playlist``` file as folders, and loads images from those folders.

## Deployment
Instructions here are specifically detailed for Raspberry Pi Raspbian.
1. Install system image packages:<br>
```sudo apt-get install python3-tk tk-dev libjpeg-progs libjpeg62-turbo libjpeg9-dev zlib1g-dev libfreetype6-dev -y```
1. Make sure you have Python 3.6 installed.<br>
If not, install from [here](https://gist.github.com/dschep/24aa61672a2092246eaca2824400d37f)
1. Download the source files to "/home/pi/Documents/jpresenter"
1. Change to the JPresenter directory<br> ```cd /home/pi/Documents/jpresenter```
1. Create "jpresenter" virtual environment:<br> ```python3 -m venv env```
1. Activate "jpresenter" virtual environment:<br> ```env/bin/activate```
1. Install python packages:<br> ```pip3 install -r requirements.txt```
1. Create the log directory:<br> ```mkdir log```
1. Add following lines to ```crontab -e```
```
@reboot /home/pi/Documents/jpresenter/scripts/jscheduler-autostart.sh  >> /home/pi/Documents/jpresenter/log/jscheduler-autostart.log 2>&1
@reboot /home/pi/Documents/jpresenter/scripts/viewer-autostart.sh  >> /home/pi/Documents/jpresenter/log/viewer-autostart.log 2>&1
0 22 * * * /home/pi/Documents/jpresenter/scripts/jscheduler-autostart.sh  >> /home/pi/Documents/jpresenter/log/jscheduler-autostart.log 2>&1
0 22 * * * /home/pi/Documents/jpresenter/scripts/viewer-autostart.sh  >> /home/pi/Documents/jpresenter/log/viewer-autostart.log 2>&1
```
Reboot, and it should work.<br>
If not, look at the log files in the ```log``` directory

##Notes
If you see a blank screen, or some images do not display, try increasing Raspberry Pi GPU memory: [memory split](https://www.raspberrypi.org/documentation/configuration/raspi-config.md)

## License
Licensed under the AGPL-3.0 License - see [LICENSE](LICENSE) for details

# Acknowledgments
* Many thanks to [@paddyg](https://www.raspberrypi.org/forums/memberlist.php?mode=viewprofile&u=9640)
* Based on [example](https://www.raspberrypi.org/forums/viewtopic.php?t=80229#p986846) given by [@paddyg](https://www.raspberrypi.org/forums/memberlist.php?mode=viewprofile&u=9640) 
