#!/usr/bin/python
# manualKBD.py
# manual keyboard control
# Author : Zachary Igielman

import RPi.GPIO as GPIO, sys, threading, time

#use physical pin numbering
GPIO.setmode(GPIO.BOARD)

#use pwm on inputs so motors don't go too fast
GPIO.setup(19, GPIO.OUT)
p=GPIO.PWM(19, 20)
p.start(0)
GPIO.setup(21, GPIO.OUT)
q=GPIO.PWM(21, 20)
q.start(0)
GPIO.setup(24, GPIO.OUT)
a=GPIO.PWM(24,20)
a.start(0)
GPIO.setup(26, GPIO.OUT)
b=GPIO.PWM(26,20)
b.start(0)

fastspeed = 60

def straight():
  p.ChangeDutyCycle(fastspeed)
  q.ChangeDutyCycle(0)
  b.ChangeDutyCycle(fastspeed)
  a.ChangeDutyCycle(0)
  print('straight')

def turnleft():
  p.ChangeDutyCycle(0)
  q.ChangeDutyCycle(0)
  b.ChangeDutyCycle(fastspeed)
  a.ChangeDutyCycle(0)
  print('left')

def turnright():
  p.ChangeDutyCycle(fastspeed)
  q.ChangeDutyCycle(0)
  b.ChangeDutyCycle(0)
  a.ChangeDutyCycle(0)
  print('right')

def stopall():
  p.ChangeDutyCycle(0)
  q.ChangeDutyCycle(0)
  b.ChangeDutyCycle(0)
  a.ChangeDutyCycle(0)
  print('stop')

#make a global variable to communcate between sonar function and main loop
globalstop=0
Going=True

def sonar():
  while Going:
    global globalstop
    GPIO_TRIGGER=8
    GPIO_ECHO=8
    GPIO.setup(8,GPIO.OUT)
    # Send 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()
    count=time.time()
    GPIO.setup(8,GPIO.IN)
    while GPIO.input(GPIO_ECHO)==0 and time.time()-count<0.1:
      start = time.time()
    stop=time.time()
    while GPIO.input(GPIO_ECHO)==1:
      stop = time.time()
    # Calculate pulse length
    elapsed = stop-start
    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34000
    # That was the distance there and back so halve the value
    distance = distance / 2
    if distance<10:
      globalstop=1
      print("Too close")
    else:
      globalstop=0
      print("Far")
    time.sleep(1)

threading.Timer(1, sonar).start()

# main loop
try:
  while True:
    if globalstop==1:
      stopall()
    else:
      testVar = raw_input("What direction (press letter then enter)? (w: forward, a: left, d: right, s: stop)")
      if testVar=="a":
        turnleft()
      elif testVar=="d":
        turnright()
      elif testVar=="w":
        straight()
      elif testVar=="s":
        stopall()
    time.sleep(0.01)
except KeyboardInterrupt:
  Going = False
  GPIO.cleanup()
  sys.exit()
