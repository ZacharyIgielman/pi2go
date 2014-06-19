#!/usr/bin/python
# servoTest.py

import pi2go

# Define pins for Pan/Tilt
pan = 0
tilt = 1
tVal = 0 # 0 degrees is centre
pVal = 0 # 0 degrees is centre

pi2go.init()
print "Pi2Go version: ", pi2go.version()

def doServos():
    pi2go.setServo(pan, pVal)
    pi2go.setServo(tilt, tVal)

try:
    while True:
        key=raw_input("Move Pan/Tilt Servos W-Up, Z-Down, A-Left, S-Right Space=Centre, X=Stop:")
        if key==" ":
            tVal = 0
            pVal = 0
            doServos()
            print "Centre"

        if key=="x":
            pi2go.stopServos()
            print "Stop"

        elif key=="w":
            pVal -= 10
            doServos()
            print "Up"

        elif key=="a":
            tVal -= 10
            doServos()
            print "Left"

        elif key=="s":
            tVal += 10
            doServos()
            print "Right"

        elif key=="z":
            pVal += 10
            doServos()
            print "Down"

        elif key=="g":
            pi2go.startServos()
            print "Down"

except KeyboardInterrupt:
    print
    pi2go.cleanup()
