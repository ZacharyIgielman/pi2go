#!/usr/bin/python
# lightFollow.py
# chance light source using light detectors
# Author : Zachary Igielman

import RPi.GPIO as GPIO, sys, threading, time
from Adafruit_PWM_Servo_Driver import PWM
from sgh_PCF8591P import sgh_PCF8591P


# Initialise the PWM device using the default address
pwm = PWM(0x40, debug = False)
pwm.setPWMFreq(60)  # Set frequency to 60 Hz

#use physical pin numbering
GPIO.setmode(GPIO.BOARD)

#set up digital line detectors as inputs
GPIO.setup(12, GPIO.IN) # Right line sensor
GPIO.setup(13, GPIO.IN) # Left line sensor

#Set up IR obstacle sensors as inputs
GPIO.setup(7, GPIO.IN) # Left obstacle sensor
GPIO.setup(11, GPIO.IN) # Right obstacle sensor
GPIO.setup(15, GPIO.IN) # Centre Front obstacle sensor

#use pwm on inputs so motors don't go too fast
# Pins 24, 26 Left Motor
# Pins 19, 21 Right Motor
L1 = 26
L2 = 24
R1 = 19
R2 = 21

pcfADC = None
try:
    pcfADC = sgh_PCF8591P(1) #i2c, 0x48)
    print pcfADC
    print "PCF8591P Detected"
except:
    print "No PCF8591 Detected"
    
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

#make a global variable to communicate between sonar function and main loop
tooclose = False
finished = False
fast = 100
slow = 30

# Define Colour IDs for the RGB LEDs
Blue = 0
Green = 1
Red = 2
pwmMax = 4095 # maximum PWM value

def sonar():
       while finished != True:
                  global tooclose
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
                          tooclose = True
                          print("Too close")
                  else:
                          tooclose = False
                          print("Far")
                  time.sleep(1)

threading.Timer(1, sonar).start()

def setLEDs(LED, red, green, blue):
  pwm.setPWM(LED * 3 + Red, 0, pwmMax - red)
  pwm.setPWM(LED * 3 + Green, 0, pwmMax - green)
  pwm.setPWM(LED * 3 + Blue, 0, pwmMax - blue)

def setAllLEDs (red, green, blue):
  for i in range(5):
    setLEDs(i, red, green, blue)

# Switch all LEDs Off
setAllLEDs (0, 0, 0)

try:
       while True:
                  try:
                    frontLeft  = pcfADC.readADC(0) # get all light readings
                    time.sleep(0.01)
                    frontRight = pcfADC.readADC(1)
                    time.sleep(0.01)
                    rearLeft   = pcfADC.readADC(2)
                    time.sleep(0.01)
                    rearRight  = pcfADC.readADC(3)
                    time.sleep(0.01)
                  except:
                    time.sleep(0.1)
                  if tooclose == True:
                          p.ChangeDutyCycle(0)
                          q.ChangeDutyCycle(fast)
                          a.ChangeDutyCycle(0)
                          b.ChangeDutyCycle(fast)
                          setAllLEDs(0, 0, 0)    # switch all LEDs On for Reverse
                          print('reverse')
                          time.sleep(1)
                          p.ChangeDutyCycle(0)
                          q.ChangeDutyCycle(fast)
                          a.ChangeDutyCycle(fast)
                          b.ChangeDutyCycle(0)
                          setAllLEDs(0, pwmMax, 0) # Turn LEDs Green for Spin
                          print('spin')
                          time.sleep(1)
                          tooclase = False
                  if GPIO.input(7)==0 or GPIO.input(11)==0 or GPIO.input(15)==0:
                          p.ChangeDutyCycle(0)
                          q.ChangeDutyCycle(0)
                          a.ChangeDutyCycle(0)
                          b.ChangeDutyCycle(0)
                          setAllLEDs(0, 0, 0)    # switch all LEDs Off for Stop
                          print('stop')
                  elif (frontLeft + frontRight) < (rearLeft + rearRight):
                          p.ChangeDutyCycle(fast)
                          q.ChangeDutyCycle(0)
                          a.ChangeDutyCycle(0)
                          b.ChangeDutyCycle(fast)
                          setAllLEDs(0, pwmMax, 0) # Turn LEDs Green for Spin
                          print('spin')
                  elif frontLeft > (frontRight + 5): # may need to adjust this magic numnber 10
                          p.ChangeDutyCycle(slow)
                          q.ChangeDutyCycle(0)
                          a.ChangeDutyCycle(fast)
                          b.ChangeDutyCycle(0)
                          setAllLEDs(0, 0, pwmMax) # Turn LEDs Blue to Left
                          print('left')
                  elif frontRight > (frontLeft + 5): # may need to adjust this magic number 10
                          p.ChangeDutyCycle(fast)
                          q.ChangeDutyCycle(0)
                          a.ChangeDutyCycle(slow)
                          b.ChangeDutyCycle(0)
                          setAllLEDs(pwmMax, 0, 0) # Turn LEDs Red to Right
                          print('right')
                  else:
                          p.ChangeDutyCycle(fast)
                          q.ChangeDutyCycle(0)
                          a.ChangeDutyCycle(fast)
                          b.ChangeDutyCycle(0)
                          setAllLEDs(pwmMax, pwmMax, pwmMax)  # Turn LEDs White for Forwards
                          print('straight')
                  time.sleep(0.1)
except KeyboardInterrupt:
       finished = True  # stop other loops
       setAllLEDs (0, 0, 0)
       GPIO.cleanup()
       sys.exit()
