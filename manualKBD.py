import RPi.GPIO as GPIO, sys, threading, pygame
from pygame.locals import *

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# set up the window
WINDOWWIDTH = 400
WINDOWHEIGHT = 400
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Input')

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

slowspeed = 40
fastspeed = 100

def straight():
  p.ChangeDutyCycle(fastspeed)
  q.ChangeDutyCycle(0)
  b.ChangeDutyCycle(fastspeed)
  a.ChangeDutyCycle(0)
  print('straight')

def turnleft():
  p.ChangeDutyCycle(slowspeed)
  q.ChangeDutyCycle(0)
  b.ChangeDutyCycle(fastspeed)
  a.ChangeDutyCycle(0)
  print('left')

def turnright():
  p.ChangeDutyCycle(fastspeed)
  q.ChangeDutyCycle(0)
  b.ChangeDutyCycle(slowspeed)
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

GPIO.setup(7,GPIO.IN)
GPIO.setup(11,GPIO.IN)
GPIO.setup(15,GPIO.IN)

# main loop
try:
  while True:
    if globalstop=1 or GPIO.input(7)==0 or GPIO.input(11)==0 or GPIO.input(15)==0:
      stopall()
    else:
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          Going = False
          GPIO.cleanup()
          sys.exit()
        if event.type == KEYDOWN:
            # change the keyboard variables
            if event.key == K_LEFT or event.key == ord('a'):
                turnleft()
            if event.key == K_RIGHT or event.key == ord('d'):
                turnright()
            if event.key == K_UP or event.key == ord('w'):
                straight()
            if event.key == K_DOWN or event.key == ord('s'):
                stopall()
    time.sleep(0.01)
except KeyboardInterrupt:
  pygame.quit()
  Going = False
  GPIO.cleanup()
  sys.exit()
