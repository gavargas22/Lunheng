#! /usr/bin/python
# Based off the code written by Kevin Kingsbury https://github.com/kmkingsbury
# Modified by Guillermo Vargas: https://github.com/gavargas22
# License: GPL 2.0

import os
import pdb
import daemon
import time
import io
import math
import bme280 as baro

import RPi.GPIO as GPIO

from time import gmtime, strftime
import threading
# import yaml
import csv
# import rrdtool
import json

# The pin number where the anemometer is connected
anemometer = 7
# The sampling time in seconds
sampling_time = 10

# Anemometer Factor (Change this value to the correct calculated factor)
anemometer_factor = 3.2

runner = True
windspeed_count = 0

def windEventHandler(pin):
    print "handling wind speed event"
    global windspeed_count
    windspeed_count += 1
    print windspeed_count

def calculate_wind_speed_from_pulses(windspeed_count_number):
    anemometer_speed = float(anemometer_factor)*(((float(0.5*windspeed_count_number))*(float(math.pi)*float(0.0508)))/(float(10)))
    # Reduce precision of speed calculation
    reduced_precision_anemometer_speed = "%f" % round(anemometer_speed, 2)
    return reduced_precision_anemometer_speed


# Main Loop
if __name__ == '__main__':

    # Set the GPIO mode to Board
    GPIO.setmode(GPIO.BOARD)
    # Set up the kind of GPIO befavior on the anemometer pi
    GPIO.setup(anemometer, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    # tell the GPIO library to look out for an
    # event on pin x and deal with it by calling
    # the windEventHandler function
    GPIO.add_event_detect(anemometer, GPIO.FALLING)
    GPIO.add_event_callback(anemometer, windEventHandler)


    try:
        while (runner == True):
            current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

            #Wind Speed
            #interupt: 1 = 180deg, 2 int = 1 full rotation.
            windspeed = windspeed_count
            windspeed_count = 0;
            # Read the Barometer data
            temperature, pressure, humidity = baro.readBME280All()
            #Sleep
            time.sleep(10) #set to whatever
            # Build the data object
            print(current_time)
            print(windspeed_count)
            print(calculate_wind_speed_from_pulses(windspeed_count))
            print(temperature)
            print(pressure)
            print(humidity)

            #Record to CSV
            data = {
                "timestamp": current_time,
                "anemometer": {
                  "speed": calculate_wind_speed_from_pulses(windspeed_count),
                  "gusts": 0
                },
                "thermometer": {
                  "outside": temperature
                },
                "hygrometer": {
                  "relative_humidity": humidity
                },
                "barometer": {
                  "pressure": pressure,
                  "altitude": 0
                }
            }

            print(data)

            # Remove the file
            if os.path.isfile('../app/data/data.json') :
                os.remove('../app/data/data.json')
            # Create a new file
            with open('../app/data/data.json', 'w+') as weather_json:
                # json_data = json.load(weather_json)
                latest_entry = data
                # print(json_data[-1])
                json.dump(latest_entry, weather_json)
                weather_json.close


    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
        print "\nKilling Thread..."
        runner = False
        #gpsp.join() # wait for the thread to finish what it's doing
        print "Almost done."
        weather_json.close()
        GPIO.cleanup()
        print "Done.\nExiting."
        exit();
