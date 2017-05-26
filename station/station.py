#! /usr/bin/python
# Based off the code written by Kevin Kingsbury https://github.com/kmkingsbury
# Modified by Guillermo Vargas: https://github.com/gavargas22
# License: GPL 2.0

import os
import pdb
import daemon
import time
import io

import RPi.GPIO as GPIO

from time import gmtime, strftime
import threading
# import yaml
import csv
# import rrdtool
import json

anemometer = 7

runner = True
windspeed_count = 0

def windEventHandler(pin):
    print "handling wind speed event"
    global windspeed_count
    windspeed_count += 1
    print windspeed_count


# Main Loop
if __name__ == '__main__':

    # Log into JSON
    real_time_json = io.open('../app/data/data.json', mode='w', encoding='utf-8')
    json.dump([], real_time_json)

    # json_data = json.load(real_time_json)
    # real_time_json.close()

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(anemometer, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    # tell the GPIO library to look out for an
    # event on pin x and deal with it by calling
    # the buttonEventHandler function

    GPIO.add_event_detect(anemometer,GPIO.FALLING)
    GPIO.add_event_callback(anemometer,windEventHandler)


    try:
        while (runner == True):
            current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

            #Wind Speed
            #interupt: 1 = 180deg, 2 int = 1 full rotation.
            windspeed = windspeed_count
            windspeed_count = 0;


            #Record to CSV
            data = {
              current_time: {
                "timestamp": current_time,
                "anemometer": {
                  "speed": windspeed_count,
                  "gusts": 10
                },
                "thermometer": {
                  "outside": 27
                },
                "hygrometer": {
                  "relative_humidity": 0.4
                },
                "barometer": {
                  "pressure": 29.92,
                  "altitude": 3940
                }
              }
            }

            with io.open('../app/data/data.json', mode='w', encoding='utf-8') as weather_json:
                pdb.set_trace()
                latest_entry = data
                json_data.append(entry)
                json.dump(json_data, weather_json)
                weather_json.close

            #Sleep
            time.sleep(10) #set to whatever


    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
        print "\nKilling Thread..."
        runner = False
        #gpsp.join() # wait for the thread to finish what it's doing
        print "Almost done."
        real_time_json.close()
        GPIO.cleanup()
        print "Done.\nExiting."
        exit();
