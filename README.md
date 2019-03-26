This is a python script built to run off a cron job at a set period of time. This script is used on a Raspberry Pi, a Kuman Soil Moisture
Sensor Kit attached to GPIO pin 17, and a USB 5V motor attached to GPIO pin 27. At the set time in the cron job, this script will check the moiture sensor and determine if your plant needs watering. If it does, then it will power the motor for 5 seconds. As long as your motor is in water, and your motor is setup to water a plant, it will water the plant then. It will also log any waterings that it does in a log file. 

What I did in order to start the cron job is type the following...

crontab -e

...Then linux opens up my crontab file in nano. At the end of the file I put the following...

0 * * * * sudo /usr/bin/python /home/pi/water_my_plant/sensor_check.py

...This will make the script run at the top of every hour. You may choose to set the script to run at a different interval based on how 
you input this line.

Any questions, hit me up at joejoejoey13@gmail.com.
