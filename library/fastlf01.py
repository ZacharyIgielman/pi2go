#!/usr/bin/python
# fastlf01.py
# speedy line follower with LEDs using library
# Author : Zachary Igielman

import sys, time
import pi2go

pi2go.init()

slowspeed = 20
fastspeed = 100

lastleft = 0
lastright = 0

# Let's get going
pi2go.forward(fastspeed)

# main loop
try:
  while True:
    left = pi2go.irLeftLine()
    right = pi2go.irRightLine()
    if left==0 and right==0:
      pi2go.stop()
    if left == 0 and lastleft == 1:
      pi2go.turnForward(slowspeed,fastspeed)
      pi2go.setAllLEDs(0, 4095, 4095)
    elif right == 0 and lastright == 1:
      pi2go.turnForward(fastspeed,slowspeed)
      pi2go.setAllLEDs(4095, 0, 4095)
    lastleft = left
    lastright = right
    time.sleep(0.01)

except KeyboardInterrupt:
       pi2go.setAllLEDs(0, 0, 0)
       pi2go.cleanup()
       sys.exit()
