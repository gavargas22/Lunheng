#! /usr/bin/python
# Based off the code written by Kevin Kingsbury https://github.com/kmkingsbury
# Modified by Guillermo Vargas: https://github.com/gavargas22
# License: GPL 2.0

import os
from daemon import Daemon

import RPi.GPIO as GPIO

from time import gmtime, strftime
import threading
import yaml
import csv
import rrdtool




anemometer = 38


runner = True
windspeed_count = 0

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
# def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)

        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

# handle the button event
runner = False

def windEventHandler (pin):
    print "handling wind speed event"
    global windspeed_count
    windspeed_count += 1


# Main Loop
if __name__ == '__main__':

# Logger open CSV
  fp = open('test.csv', 'a')
  csv = csv.writer(fp, delimiter=',')


  GPIO.setup(anemometer, GPIO.IN, pull_up_down=GPIO.PUD_UP)


  # tell the GPIO library to look out for an
  # event on pin x and deal with it by calling
  # the buttonEventHandler function

  GPIO.add_event_detect(anemometer,GPIO.FALLING)
  GPIO.add_event_callback(anemometer,windEventHandler)


  try:
    while (runner == True):
      timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())

      #Wind Speed
      #interupt: 1 = 180deg, 2 int = 1 full rotation.
      windspeed = windspeed_count
      windspeed_count = 0;

      #Record to CSV
      data = [ timenow, windspeed ]
      csv.writerow(data)

      #Sleep
      time.sleep(1) #set to whatever

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    runner = False
    #gpsp.join() # wait for the thread to finish what it's doing
  print "Almost done."
  fp.close()
  GPIO.cleanup()
  print "Done.\nExiting."
  exit();
