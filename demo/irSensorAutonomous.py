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

MotorAfwd=GPIO.PWM(19,50)
MotorBfwd=GPIO.PWM(26,50)
MotorAbk=GPIO.PWM(21,50)
MotorBbk=GPIO.PWM(24,50)

MotorAfwd.start(0)
MotorBfwd.start(0)
MotorAbk.start(0)
MotorBbk.start(0)

while True:
  left=GPIO.input(7)
  right=GPIO.input(11)
  center=GPIO.input(15)
  if left+right+center==3:
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
    MotorAbk.ChangeDutyCycle(0)
    MotorBbk.ChangeDutyCycle(0)
    if (left==0):
      MotorAbk.ChangeDutyCycle(fast)
      MotorBbk.ChangeDutyCycle(slow)
      time.sleep(2)
    if (right==0):
      MotorAbk.ChangeDutyCycle(slow)
      MotorBbk.ChangeDutyCycle(fast)
      time.sleep(2)
    if (center==0):
      MotorAbk.ChangeDutyCycle(slow)
      MotorBbk.ChangeDutyCycle(fast)
      time.sleep(2)
