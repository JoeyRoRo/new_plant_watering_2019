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
import time, os, logging, sys
import RPi.GPIO as GPIO
from time import gmtime, strftime

WORKING_PATH = '/home/pi/water_my_plant/'
MAX_LOG_KB = 1000 # 1MB
MAX_LOGS = 1000000 # at 1MB this is 1TB of logs
WATER_THRESHOLD = 0.05

def get_avg():
    # 10 readings from the moisture sensor
    readings = [GPIO.input(17) for _ in range(10)]
    # return the average
    return sum(readings)/len(readings)


def init_gpio():
    # Set your GPIO numbering to BCM
    GPIO.setmode(GPIO.BCM)

    # Set the sensor GPIO pin to an input
    GPIO.setup(17, GPIO.IN)

    # Set the motor GPIO pin to an output
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(27, GPIO.LOW)


def get_log_name(log_num=1):
    return WORKING_PATH+'Logs/Moisture_log'+str(log_num)+'.txt'


def get_curr_log_num():
    for i in range(MAX_LOGS):
        log_name = get_log_name(i)
        # Checks for over sized log files and sets a new file if it's
        # too large
        # If the log file is larger than 1MB, increment the log_num
        # variable in order to check/make a new log file
        if not os.path.isfile(log_name):
            os.mknod(log_name)
        elif os.stat(log_name).st_size > MAX_LOG_KB:
            continue
        return i

    print('Overflowed MAX_LOGS')
    sys.exit(1)


def init_logger():
    # Sets the logging mode for the logging module
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Creates a file handler
    handler = logging.FileHandler(get_log_name(get_curr_log_num()))
    handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    return logger


def main():
    init_gpio()
    logger = init_logger()

    # Get the moiture levels from the moisture sensor and water if needed
    # Also log that it was dry and watered this hour
    if get_avg() > WATER_THRESHOLD:
        logger.info('Hourly mango sensor: dry'+ \
            ' - Watered this hour.')
        print("Motor turning on!!!")
        GPIO.output(27, GPIO.HIGH)

        time.sleep(5) # water for 5 seconds

        print("Motor turned off...")
        GPIO.output(27, GPIO.LOW)
    else: 
        # If moisture sensor is wet don't wate, just log it
        logger.info('Hourly mango sensor: wet'+ \
            ' - NOT watered this hour.')
    return 0


if __name__ == '__main__':
    sys.exit(main())