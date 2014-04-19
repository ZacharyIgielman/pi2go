import time, RPi.GPIO as GPIO, sys

speed=70

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
	if GPIO.input(7)+GPIO.input(11)+GPIO.input(15)==3:
		MotorAfwd.ChangeDutyCycle(speed)
		MotorBfwd.ChangeDutyCycle(speed)
		MotorAbk.ChangeDutyCycle(0)
		MotorBbk.ChangeDutyCycle(0)
	else:
		MotorAfwd.ChangeDutyCycle(0)
        	MotorBfwd.ChangeDutyCycle(0)
        	MotorAbk.ChangeDutyCycle(10)
        	MotorBbk.ChangeDutyCycle(10)
		time.sleep(1)
		MotorAbk.ChangeDutyCycle(0)
        	MotorBbk.ChangeDutyCycle(0)
		if (GPIO.input(7)==0): #left
	        	MotorAbk.ChangeDutyCycle(speed)
        		MotorBbk.ChangeDutyCycle(speed)
			time.sleep(1)
			MotorAbk.ChangeDutyCycle(0)
        		MotorBbk.ChangeDutyCycle(0)
                	time.sleep(1)
        	if (GPIO.input(11)==0): #right
                	MotorAbk.ChangeDutyCycle(speed)
                	MotorBbk.ChangeDutyCycle(speed)
                	time.sleep(1)
                	MotorAbk.ChangeDutyCycle(0)
                	MotorBbk.ChangeDutyCycle(0)
                	time.sleep(1)
        	if (GPIO.input(15)==0): #center
                	MotorAbk.ChangeDutyCycle(speed)
                	MotorBbk.ChangeDutyCycle(speed)
                	time.sleep(1)
                	MotorAbk.ChangeDutyCycle(0)
                	MotorBbk.ChangeDutyCycle(0)
                	time.sleep(1)

