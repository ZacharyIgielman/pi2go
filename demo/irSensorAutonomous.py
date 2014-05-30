#!/usr/bin/python
# irSensorAutonomous.py
# navigator using ir obstacle detectors
# Author : Zachary Igielman

import time, RPi.GPIO as GPIO, sys

fast=50
slow=30

GPIO.setmode(GPIO.BOARD)

GPIO.setup(7,GPIO.IN)
GPIO.setup(11,GPIO.IN)
GPIO.setup(15,GPIO.IN)

GPIO.setup(19,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)

a=GPIO.PWM(19,50)
p=GPIO.PWM(26,50)
b=GPIO.PWM(21,50)
q=GPIO.PWM(24,50)

a.start(0)
p.start(0)
b.start(0)
q.start(0)

while True:
  left=GPIO.input(7)
  right=GPIO.input(11)
  center=GPIO.input(15)
  if left+right+center==3:
    a.ChangeDutyCycle(fast)
    p.ChangeDutyCycle(fast)
    b.ChangeDutyCycle(0)
    q.ChangeDutyCycle(0)
  else:
    a.ChangeDutyCycle(0)
    p.ChangeDutyCycle(0)
    b.ChangeDutyCycle(slow)
    q.ChangeDutyCycle(slow)
    time.sleep(0.5)
    b.ChangeDutyCycle(0)
    q.ChangeDutyCycle(0)
    if (left==0):
      b.ChangeDutyCycle(fast)
      q.ChangeDutyCycle(slow)
      time.sleep(2)
    if (right==0):
      b.ChangeDutyCycle(slow)
      q.ChangeDutyCycle(fast)
      time.sleep(2)
    if (center==0):
      b.ChangeDutyCycle(slow)
      q.ChangeDutyCycle(fast)
      time.sleep(2)
