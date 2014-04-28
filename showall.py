import RPi.GPIO as GPIO, sys, threading, time
from Adafruit_PWM_Servo_Driver import PWM

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
globalstop=0
finished = False
fast = 40
slow = 30

# Define Colour IDs for the RGB LEDs
Blue = 0
Red = 1
Green = 2
pwmMax = 4095 # maximum PWM value

def sonar():
       while finished != True:
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
                  if GPIO.input(12)==1 and GPIO.input(13)==1 or globalstop==1 or GPIO.input(7)==0 or GPIO.input(11)==0 or GPIO.input(15)==0:
#                  if False:
                          p.ChangeDutyCycle(0)
                          q.ChangeDutyCycle(0)
                          a.ChangeDutyCycle(0)
                          b.ChangeDutyCycle(0)
                          setAllLEDs(0, 0, 0)    # switch all LEDs Off for Stop
                          print('stop')
                  elif GPIO.input(12)==0 and GPIO.input(13)==0:
                          p.ChangeDutyCycle(fast)
                          q.ChangeDutyCycle(0)
                          a.ChangeDutyCycle(fast)
                          b.ChangeDutyCycle(0)
                          setAllLEDs(pwmMax, pwmMax, pwmMax)  # Turn LEDs White for Forwards
                          print('straight')
                  elif GPIO.input(13)==1:
                          p.ChangeDutyCycle(fast)
                          q.ChangeDutyCycle(0)
                          a.ChangeDutyCycle(0)
                          b.ChangeDutyCycle(fast)
                          setAllLEDs(pwmMax, 0, 0) # Turn LEDs Red for Right
                          print('right')
                  elif GPIO.input(12)==1:
                          p.ChangeDutyCycle(0)
                          q.ChangeDutyCycle(fast)
                          a.ChangeDutyCycle(fast)
                          b.ChangeDutyCycle(0)
                          setAllLEDs(0, 0, pwmMax) # Turn LEDs Blue to Left
                          print('left')
except KeyboardInterrupt:
       finished = True  # stop other loops
       setAllLEDs (0, 0, 0)
       GPIO.cleanup()
       sys.exit()
