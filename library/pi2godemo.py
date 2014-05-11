#!/usr/bin/python
#
# Pi2Go Demo Code using the Pi2Go library
#
# Created by Gareth Davies, May 2014
# Copyright 4tronix
#
# This code is in the public domain and may be freely copied and used
# No warranty is provided or implied
#
#======================================================================

import pi2go, time

pi2go.init()

pi2go.setAllLEDs(0, 0, 4095)

light = pi2go.getLight(0)
print light

middle = pi2go.irCentre()
print middle

distance = pi2go.getDistance()
print distance

time.sleep (3)

pi2go.cleanup()
