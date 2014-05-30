#!/usr/bin/python
# fastlf01.py
# speedy line follower and searcher
# Author : Zachary Igielman

import RPi.GPIO as GPIO, sys, threading, time

#use physical pin numbering
GPIO.setmode(GPIO.BOARD)

#set up digital line detectors as inputs
# left line sensor. 0=white, 1=black
GPIO.setup(12, GPIO.IN)
# right line sensor. 0=white, 1=black
GPIO.setup(13, GPIO.IN)

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

slowspeed = 20
fastspeed = 100
LED1 = 22
LED2 = 18
LED3 = 11
LED4 = 07
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)
GPIO.setup(LED4, GPIO.OUT)

def straight():
  p.ChangeDutyCycle(fastspeed)
  q.ChangeDutyCycle(0)
  b.ChangeDutyCycle(fastspeed)
  a.ChangeDutyCycle(0)
  setLEDs(1, 0, 0, 1)
  print('straight')

def turnright():
  p.ChangeDutyCycle(0)
  q.ChangeDutyCycle(slowspeed)
  b.ChangeDutyCycle(fastspeed)
  a.ChangeDutyCycle(0)
  setLEDs(0, 0, 1, 1)
  print('left')

def turnleft():
  p.ChangeDutyCycle(fastspeed)
  q.ChangeDutyCycle(0)
  b.ChangeDutyCycle(0)
  a.ChangeDutyCycle(slowspeed)
  setLEDs(1, 1, 0, 0)
  print('right')

def stopall():
  p.ChangeDutyCycle(0)
  q.ChangeDutyCycle(0)
  b.ChangeDutyCycle(0)
  a.ChangeDutyCycle(0)
  setLEDs(1, 1, 1, 1)
  print('stop')

def setLEDs(L1, L2, L3, L4):
  GPIO.output(LED1, L1)
  GPIO.output(LED2, L2)
  GPIO.output(LED3, L3)
  GPIO.output(LED4, L4)

setLEDs(1, 1, 1, 1)

lastleft = 0
lastright = 0

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
                  if distance<20:
                          globalstop=1
                          print("Too close")
                  else:
                          globalstop=0
                          print("Far")
                  time.sleep(1)

# ignore sonar for now
#threading.Timer(1, sonar).start()

#GPIO.setup(7,GPIO.IN)
#GPIO.setup(11,GPIO.IN)
#GPIO.setup(15,GPIO.IN)

# Let's get going
straight()

# main loop
try:
  while True:
    left = GPIO.input(12)
    right = GPIO.input(13)
    if left==1 and right==1 or globalstop==1:
      stopall()
    if left == 1 and lastleft == 0:
      turnleft()
    elif right == 1 and lastright == 0:
      turnright()
    lastleft = left
    lastright = right
    time.sleep(0.01)

except KeyboardInterrupt:
       Going = False
       GPIO.cleanup()
       sys.exit()
