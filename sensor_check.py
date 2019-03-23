#!/usr/bin/python

'''
This is a python script built to run off a cron job at a set period
of time. This script is used on a Raspberry Pi, a Kuman Soil Moisture
Sensor Kit attached to GPIO pin 17, and a USB 5V motor attached to GPIO
pin 27. At the set time in the cron job, this script will check the
moiture sensor and determine if your plant needs watering. If it does,
then it will power the motor for 3 seconds. As long as your motor is in
water, and your motor is setup to water a plant, it will water the plant
then. It will also log any waterings that it does in a log file. Any
questions, hit me up at joejoejoey13@gmail.com.

Peace!
'''

import time, os, logging
import RPi.GPIO as GPIO
from time import gmtime, strftime

# Set your GPIO numbering to BCM
GPIO.setmode(GPIO.BCM)

# Set the sensor GPIO pin to an input
GPIO.setup(17, GPIO.IN)

# Set the motor GPIO pin to an output
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.LOW)

# Sets the logging mode for the logging module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# creates a file handler
log_num = 1
handler = logging.FileHandler('./Logs/Moisture_log'+str(log_num)+'.txt')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

def get_avg():
        # Saves 10 readings from the moisture sensor, then takes the
        # average and saves it as variable 'm'
        readings = []
        num_readings = 10
        while num_readings > 0:
                # Get the current reading from the sensor, sensor will
                # provide 1 if it's dry, and a 0 if it is wet
                readings.append(GPIO.input(17))
                num_readings = num_readings - 1
        m = sum(readings)/len(readings)
        return m

# Get average of ten readings from the sensor and if it's mostly dry...
#print("Checking sensor...")
#print(str(get_avg()))
#raw_input("Here is average sensor.")
m = int(get_avg())
if m > .05:
#    raw_input("Sensor is dry! watering and logging")
    while True:
        # Checks for over sized log files and sets a new file if it's
        # too large
        statinfo = os.stat('./Logs/Moisture_log'+str(log_num)+'.txt')
        file_size = statinfo.st_size
        # If the log file is larger than 1MB, increment the log_num
        # variable in order to check/make a new log file
        if int(file_size) > 1000:
            log_num = log_num + 1
            handler = logging.FileHandler('./Logs/Moisture_log' \
            +str(log_num)+'.txt')
        else: break
    logger.info('Hourly - Mango sensor: Moisture '+ \
        'sensor is dry - Watered this hour. \n')
#    print("Motor turning on!!!")
#    GPIO.output(27, GPIO.HIGH)
    time.sleep(3)
#    print("Motor turned off...")
#    GPIO.output(27, GPIO.LOW)
#else: raw_input("Sensor is wet. Not watering and not logging.")
