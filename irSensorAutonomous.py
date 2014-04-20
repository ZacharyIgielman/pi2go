import time, RPi.GPIO as GPIO, sys

fast=100
slow=50

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

while True:
	if GPIO.input(7)+GPIO.input(11)+GPIO.input(15)==3:
		MotorAfwd.start(fast)
		MotorBfwd.start(fast)
		MotorAbk.stop(0)
		MotorBbk.stop(0)
	else:
		MotorAfwd.stop(0)
        	MotorBfwd.stop(0)
        	MotorAbk.start(10)
        	MotorBbk.start(10)
		time.sleep(1)
		MotorAbk.stop(0)
        	MotorBbk.stop(0)
		if (GPIO.input(7)==0): #left
	        	MotorAbk.start(slow)
        		MotorBbk.start(fast)
			time.sleep(1)
        	if (GPIO.input(11)==0): #right
                	MotorAbk.start(fast)
                	MotorBbk.start(slow)
                	time.sleep(1)
        	if (GPIO.input(15)==0): #center
                	MotorAbk.start(slow)
                	MotorBbk.start(fast)
                	time.sleep(1)

