
#!/usr/bin/python

import smbus
import math
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(17,0)
GPIO.setup(18,0)
GPIO.setup(22,0)
GPIO.setup(23,0)

motor1a=GPIO.PWM(17,100)
motor1b=GPIO.PWM(18,100)
motor2a=GPIO.PWM(22,100)
motor2b=GPIO.PWM(23,100)

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

upright=read_word_2c(0x43)
print "Upright="+str(upright)
offset=5

listOfX=[upright,upright,upright,upright,upright,upright]

while True:
	listOfX.pop()
	listOfX.insert(0,read_word_2c(0x43))
	y=(listOfX[0]+listOfX[1]+listOfX[2]+listOfX[3]+listOfX[4])/5
	print str(y)
        speed=0.5*abs(y-upright)
        if speed>100:
                speed=100
        if y > upright+offset:
                motor1a.stop()
                motor1b.start(speed)
                motor2a.stop()
                motor2b.start(speed)
        elif y < upright-offset:
                motor1a.start(speed)
                motor1b.stop()
                motor2a.start(speed)
                motor2b.stop()
        else:
                motor1a.stop()
                motor1b.stop()
                motor2a.stop()
                motor2b.stop()
