#!/usr/bin/python
# ultrasonicPi2Go.py
# Measure distance using the ultrasonic module with Pi2Go
#
# Author : Zachary Igielman
# Date   : 1/4/2014 (I know, but it’s not an April fools!)

# Import required Python libraries
import time
import RPi.GPIO as GPIO

fast=50
slow=30

# Use physical pin numbers
GPIO.setmode(GPIO.BOARD)

# Define GPIO to use on Pi
GPIO_TRIGGER = 8
GPIO_ECHO    = 8

GPIO.setup(19,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)

MotorAfwd=GPIO.PWM(19,50)
MotorBfwd=GPIO.PWM(26,50)
MotorAbk=GPIO.PWM(21,50)
MotorBbk=GPIO.PWM(24,50)

MotorAfwd.start(0)
MotorBfwd.start(0)
MotorAbk.start(0)
MotorBbk.start(0)

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

# Allow module to settle
time.sleep(0.5)

while True:
  # Send 10us pulse to trigger
  GPIO.output(GPIO_TRIGGER, True)
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)
  start = time.time()
  count=time.time()
  GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo
  while GPIO.input(GPIO_ECHO)==0 and time.time()-count<1:
    start = time.time()

  while GPIO.input(GPIO_ECHO)==1:
    stop = time.time()

  # Calculate pulse length
  elapsed = stop-start

  # Distance pulse travelled in that time is time
  # multiplied by the speed of sound (cm/s)
  distance = elapsed * 34300

  # That was the distance there and back so halve the value
  distance = distance / 2

  if distance>10:
    MotorAfwd.ChangeDutyCycle(fast)
    MotorBfwd.ChangeDutyCycle(fast)
    MotorAbk.ChangeDutyCycle(0)
    MotorBbk.ChangeDutyCycle(0)
  else:
    MotorAfwd.ChangeDutyCycle(0)
    MotorBfwd.ChangeDutyCycle(0)
    MotorAbk.ChangeDutyCycle(slow)
    MotorBbk.ChangeDutyCycle(slow)
    time.sleep(0.5)
    MotorAbk.ChangeDutyCycle(fast)
    MotorBbk.ChangeDutyCycle(slow)
    time.sleep(2)

# Reset GPIO settings
GPIO.cleanup()
