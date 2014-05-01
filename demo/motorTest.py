# Pi2Go Motor Test
# Moves: Forward, Reverse, turn Right, turn Left, Stop - then repeat
# Press Ctrl-C to stop
#
# Also demonstrates writing to the LEDs
#
# To check wiring is correct ensure the order of movement as above is correct
# Run using: sudo python motorTest.py


import RPi.GPIO as GPIO, sys, threading, time
from Adafruit_PWM_Servo_Driver import PWM

# Initialise the PWM device using the default address
pwm = PWM(0x40, debug = False)
pwm.setPWMFreq(60)  # Set frequency to 60 Hz

#use physical pin numbering
GPIO.setmode(GPIO.BOARD)

#use pwm on inputs so motors don't go too fast
# Pins 24, 26 Left Motor
# Pins 19, 21 Right Motor
L1 = 26
L2 = 24
R1 = 19
R2 = 21

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

slowspeed = 20
fastspeed = 50

# Define Colour IDs for the RGB LEDs
Blue = 0
Red = 1
Green = 2
pwmMax = 4095 # maximum PWM value

def forwards():
  p.ChangeDutyCycle(fastspeed)
  q.ChangeDutyCycle(0)
  a.ChangeDutyCycle(fastspeed)
  b.ChangeDutyCycle(0)
  setAllLEDs(pwmMax, pwmMax, pwmMax) # Turn LEDs White for forwards
  print('straight')

def reverse():
  p.ChangeDutyCycle(0)
  q.ChangeDutyCycle(fastspeed)
  a.ChangeDutyCycle(0)
  b.ChangeDutyCycle(fastspeed)
  setAllLEDs(0, pwmMax, 0) # Turn LEDs Green for reverse
  print('reverse')

def spinleft():
  p.ChangeDutyCycle(0)
  q.ChangeDutyCycle(fastspeed)
  a.ChangeDutyCycle(fastspeed)
  b.ChangeDutyCycle(0)
  setAllLEDs(0, 0, pwmMax)  # Turn LEDs Blue for left
  print('left')

def spinright():
  p.ChangeDutyCycle(fastspeed)
  q.ChangeDutyCycle(0)
  a.ChangeDutyCycle(0)
  b.ChangeDutyCycle(fastspeed)
  setAllLEDs(pwmMax, 0, 0)  # Turn LEDs Red for right
  print('right')

def stopall():
  p.ChangeDutyCycle(0)
  q.ChangeDutyCycle(0)
  a.ChangeDutyCycle(0)
  b.ChangeDutyCycle(0)
  setAllLEDs(0, 0, 0)  # Turn LEDs Off for stop
  print('stop')

def setLEDs(LED, red, green, blue):
  pwm.setPWM(LED * 3 + Red, 0, pwmMax - red)
  pwm.setPWM(LED * 3 + Green, 0, pwmMax - green)
  pwm.setPWM(LED * 3 + Blue, 0, pwmMax - blue)

def setAllLEDs (red, green, blue):
  for i in range(5):
    setLEDs(i, red, green, blue)

# Switch all LEDs Off
setAllLEDs (0, 0, 0)


# main loop
try:
  while True:
    forwards()
    time.sleep(3)
    reverse()
    time.sleep(3)
    spinright()
    time.sleep(3)
    spinleft()
    time.sleep(3)
    stopall()
    time.sleep(3)

except KeyboardInterrupt:
       Going = False
       setAllLEDs(0, 0, 0)
       GPIO.cleanup()
       sys.exit()
