#!/usr/bin/env python
# Based off the code written by Dan Mandle http://dan.mandle.me September 2012
# Modified by Guillermo Vargas: https://github.com/gavargas22
# License: GPL 2.0

import os
from daemon import Daemon

import RPi.GPIO as GPIO
import pigpio

from time import gmtime, strftime
import threading
import yaml
import csv
import rrdtool


anemometer = 38

cb = [0]*NGPIO
last = [0]*NGPIO
now = [0]*NGPIO

pi = pigpio.pi()

for i in range(NGPIO):
   pi.set_PWM_frequency(GPIO[i], 100000) # set maximum frequency.
   pi.set_PWM_dutycycle(GPIO[i], 128) # square wave.
   cb[i] = pi.callback(GPIO[i])
   last[i] = 0

while True:

   time.sleep(1.0)
   total = 0
   for i in range(NGPIO):
      now[i] = cb[i].tally()
      total = total + now[i] - last[i]
      last[i] = now[i]
   print(total)
