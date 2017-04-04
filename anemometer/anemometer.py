#!/usr/bin/env python

import time

import pigpio

GPIO=[4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

NGPIO = len(GPIO)

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
