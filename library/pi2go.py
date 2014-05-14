#!/usr/bin/python
#
# Python Module to externalise all Pi2Go specific hardware
#
# Created by Gareth Davies, May 2014
# Copyright 4tronix
#
# This code is in the public domain and may be freely copied and used
# No warranty is provided or implied
#
#======================================================================


#======================================================================
# General Functions
#
# init(). Initialises GPIO pins, switches motors and LEDs Off, etc
# cleanup(). Sets all motors and LEDs off and sets GPIO to standard values
#======================================================================


#======================================================================
# Motor Functions
#
# stop(): Stops both motors
# forward(speed): Sets both motors to move forward at speed. 0 <= speed <= 100
# reverse(speed): Sets both motors to reverse at speed. 0 <= speed <= 100
# spinLeft(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
# spinRight(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
# turnForward(leftSpeed, rightSpeed): Moves forwards in an arc by setting different speeds. 0 <= leftSpeed,rightSpeed <= 100
# turnreverse(leftSpeed, rightSpeed): Moves backwards in an arc by setting different speeds. 0 <= leftSpeed,rightSpeed <= 100
#======================================================================


#======================================================================
# RGB LED Functions
#
# setLED(LED, Red, Green, Blue): Sets the LED specified to required RGB value. 0 >= LED <= 4; 0 <= R,G,B <= 4095
# setAllLEDs(Red, Green, Blue): Sets all LEDs to required RGB. 0 <= R,G,B <= 4095
#======================================================================


#======================================================================
# IR Sensor Functions
#
# irLeft(): Returns state of Left IR Obstacle sensor
# irRight(): Returns state of Right IR Obstacle sensor
# irCentre(): Returns state of Centre IR Obstacle sensor
# irAll(): Returns true if any of the Obstacle sensors are triggered
# irLeftLine(): Returns state of Left IR Line sensor
# irRightLine(): Returns state of Right IR Line sensor
#======================================================================


#======================================================================
# UltraSonic Functions
#
# getDistance(). Returns the distance in cm to the nearest reflecting object. 0 == no object
#======================================================================


#======================================================================
# Light Sensor Functions
#
# getLight(Sensor). Returns the value 0..1023 for the selected sensor, 0 <= Sensor <= 3
# getLightFL(). Returns the value 0..1023 for Front-Left light sensor
# getLightFR(). Returns the value 0..1023 for Front-Right light sensor
# getLightBL(). Returns the value 0..1023 for Back-Left light sensor
# getLightBR(). Returns the value 0..1023 for Back-Right light sensor
#======================================================================


# Import all necessary libraries
import RPi.GPIO as GPIO, sys, threading, time
from Adafruit_PWM_Servo_Driver import PWM
from sgh_PCF8591P import sgh_PCF8591P

# Pins 24, 26 Left Motor
# Pins 19, 21 Right Motor
L1 = 26
L2 = 24
R1 = 19
R2 = 21

# Define obstacle sensors and line sensors
irFL = 7
irFR = 11
irMID = 15
lineRight = 13
lineLeft = 12

# Define Colour IDs for the RGB LEDs
Blue = 0
Green = 1
Red = 2
pwmMax = 4095 # maximum PWM value

# Define Sonar Pin (same pin for both Ping and Echo
sonar = 8


#======================================================================
# General Functions
#
# init(). Initialises GPIO pins, switches motors and LEDs Off, etc
def init():
    global p, q, a, b, pwm, pcfADC
    # Initialise the PWM device using the default address
    pwm = PWM(0x40, debug = False)
    pwm.setPWMFreq(60)  # Set frequency to 60 Hz

    #use physical pin numbering
    GPIO.setmode(GPIO.BOARD)

    #set up digital line detectors as inputs
    GPIO.setup(lineRight, GPIO.IN) # Right line sensor
    GPIO.setup(lineLeft, GPIO.IN) # Left line sensor

    #Set up IR obstacle sensors as inputs
    GPIO.setup(irFL, GPIO.IN) # Left obstacle sensor
    GPIO.setup(irFR, GPIO.IN) # Right obstacle sensor
    GPIO.setup(irMID, GPIO.IN) # Centre Front obstacle sensor

    #use pwm on inputs so motors don't go too fast
    GPIO.setup(L1, GPIO.OUT)
    p = GPIO.PWM(L1, 20)
    p.start(0)

    GPIO.setup(L2, GPIO.OUT)
    q = GPIO.PWM(L2, 20)
    q.start(0)

    GPIO.setup(R1, GPIO.OUT)
    a = GPIO.PWM(R1, 20)
    a.start(0)

    GPIO.setup(R2, GPIO.OUT)
    b = GPIO.PWM(R2, 20)
    b.start(0)

    # Initalise the ADC
    pcfADC = None # ADC object
    try:
        pcfADC = sgh_PCF8591P(1) #i2c, 0x48)
        print pcfADC
        print "PCF8591P Detected"
    except:
        print "No PCF8591 Detected"


# cleanup(). Sets all motors and LEDs off and sets GPIO to standard values
def cleanup():
    stop()
    setAllLEDs(0, 0, 0)
    GPIO.cleanup()
# End of General Functions
#======================================================================


#======================================================================
# Motor Functions
#
# stop(): Stops both motors
def stop():
    p.ChangeDutyCycle(0)
    q.ChangeDutyCycle(0)
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle(0)
    
# forward(speed): Sets both motors to move forward at speed. 0 <= speed <= 100
def forward(speed):
    p.ChangeDutyCycle(speed)
    q.ChangeDutyCycle(0)
    a.ChangeDutyCycle(speed)
    b.ChangeDutyCycle(0)
    
# reverse(speed): Sets both motors to reverse at speed. 0 <= speed <= 100
def reverse(speed):
    p.ChangeDutyCycle(0)
    q.ChangeDutyCycle(speed)
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle(speed)

# spinLeft(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
def spinLeft(speed):
    p.ChangeDutyCycle(0)
    q.ChangeDutyCycle(speed)
    a.ChangeDutyCycle(speed)
    b.ChangeDutyCycle(0)
    
# spinRight(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
def spinRight(speed):
    p.ChangeDutyCycle(speed)
    q.ChangeDutyCycle(0)
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle(speed)
    
# turnForward(leftSpeed, rightSpeed): Moves forwards in an arc by setting different speeds. 0 <= leftSpeed,rightSpeed <= 100
def turnForward(leftSpeed, rightSpeed):
    p.ChangeDutyCycle(leftSpeed)
    q.ChangeDutyCycle(0)
    a.ChangeDutyCycle(rightSpeed)
    b.ChangeDutyCycle(0)
    
# turnReverse(leftSpeed, rightSpeed): Moves backwards in an arc by setting different speeds. 0 <= leftSpeed,rightSpeed <= 100
def turnReverse(leftSpeed, rightSpeed):
    p.ChangeDutyCycle(0)
    q.ChangeDutyCycle(leftSpeed)
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle(rightSpeed)

# End of Motor Functions
#======================================================================


#======================================================================
# RGB LED Functions
#
# setLED(LED, Red, Green, Blue): Sets the LED specified to required RGB value. 0 >= LED <= 4; 0 <= R,G,B <= 4095
def setLEDs(LED, red, green, blue):
  pwm.setPWM(LED * 3 + Red, 0, pwmMax - red)
  pwm.setPWM(LED * 3 + Green, 0, pwmMax - green)
  pwm.setPWM(LED * 3 + Blue, 0, pwmMax - blue)

# setAllLEDs(Red, Green, Blue): Sets all LEDs to required RGB. 0 <= R,G,B <= 4095
def setAllLEDs (red, green, blue):
  for i in range(5):
    setLEDs(i, red, green, blue)

# End of RGB LED Functions
#======================================================================


#======================================================================
# IR Sensor Functions
#
# irLeft(): Returns state of Left IR Obstacle sensor
def irLeft():
    if GPIO.input(irFL)==0:
        return True
    else:
        return False
    
# irRight(): Returns state of Right IR Obstacle sensor
def irRight():
    if GPIO.input(irFR)==0:
        return True
    else:
        return False
    
# irCentre(): Returns state of Centre IR Obstacle sensor
def irCentre():
    if GPIO.input(irMID)==0:
        return True
    else:
        return False
    
# irAll(): Returns true if any of the Obstacle sensors are triggered
def irAll():
    if GPIO.input(irFL)==0 or GPIO.input(irFR)==0 or GPIO.input(irMID)==0:
        return True
    else:
        return False
    
# irLeftLine(): Returns state of Left IR Line sensor
def irLeftLine():
    if GPIO.input(lineLeft)==0:
        return True
    else:
        return False
    
# irRightLine(): Returns state of Right IR Line sensor
def irRightLine():
    if GPIO.input(lineRight)==0:
        return True
    else:
        return False
    
# End of IR Sensor Functions
#======================================================================


#======================================================================
# UltraSonic Functions
#
# getDistance(). Returns the distance in cm to the nearest reflecting object. 0 == no object
def getDistance():
    GPIO.setup(sonar, GPIO.OUT)
    # Send 10us pulse to trigger
    GPIO.output(sonar, True)
    time.sleep(0.00001)
    GPIO.output(sonar, False)
    start = time.time()
    count=time.time()
    GPIO.setup(sonar,GPIO.IN)
    while GPIO.input(sonar)==0 and time.time()-count<0.1:
        start = time.time()
    count=time.time()
    stop=count
    while GPIO.input(sonar)==1 and time.time()-count<0.1:
        stop = time.time()
    # Calculate pulse length
    elapsed = stop-start
    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34000
    # That was the distance there and back so halve the value
    distance = distance / 2
    return distance

# End of UltraSonic Functions    
#======================================================================


#======================================================================
# Light Sensor Functions
#
# getLight(sensor). Returns the value 0..1023 for the selected sensor, 0 <= Sensor <= 3
def getLight(sensor):
    value  = pcfADC.readADC(sensor)
    return value

# getLightFL(). Returns the value 0..1023 for Front-Left light sensor
def getLightFL():
    value  = pcfADC.readADC(0)
    return value

# getLightFR(). Returns the value 0..1023 for Front-Right light sensor
def getLightFR(sensor):
    value  = pcfADC.readADC(1)
    return value

# getLightBL(). Returns the value 0..1023 for Back-Left light sensor
def getLightBL(sensor):
    value  = pcfADC.readADC(2)
    return value

# getLightBR(). Returns the value 0..1023 for Back-Right light sensor
def getLightBR(sensor):
    value  = pcfADC.readADC(3)
    return value

# End of Light Sensor Functions
#======================================================================

