import RPi.GPIO as GPIO, sys, threading, time

#use physical pin numbering
GPIO.setmode(GPIO.BOARD)

#set up digital line detectors as inputs
GPIO.setup(12, GPIO.IN)
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

#make a global variable to communicate between sonar function and main loop
globalstop=0
finished = False
fast = 20
slow = 10
LED1 = 22
LED2 = 18
LED3 = 11
LED4 = 07
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)
GPIO.setup(LED4, GPIO.OUT)

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

#threading.Timer(1, sonar).start()

#GPIO.setup(7,GPIO.IN)
#GPIO.setup(11,GPIO.IN)
#GPIO.setup(15,GPIO.IN)

def setLEDs(L1, L2, L3, L4):
  GPIO.output(LED1, L1)
  GPIO.output(LED2, L2)
  GPIO.output(LED3, L3)
  GPIO.output(LED4, L4)

setLEDs(1, 1, 1, 1)

try:
       while True:
                  if GPIO.input(12)==1 and GPIO.input(13)==1 or globalstop==1:
                          a.ChangeDutyCycle(0)
                          b.ChangeDutyCycle(0)
                          p.ChangeDutyCycle(0)
                          q.ChangeDutyCycle(0)
                          setLEDs(1, 1, 1, 1)
                          print('stop')
                  elif GPIO.input(12)==0 and GPIO.input(13)==0:
                          p.ChangeDutyCycle(fast)
                          q.ChangeDutyCycle(0)
                          b.ChangeDutyCycle(fast)
                          a.ChangeDutyCycle(0)
                          setLEDs(1, 0, 0, 1)
                          print('straight')
                  elif GPIO.input(12)==1:
                          q.ChangeDutyCycle(0)
                          p.ChangeDutyCycle(fast)
                          a.ChangeDutyCycle(fast)
                          b.ChangeDutyCycle(0)
                          setLEDs(1, 1, 0, 0)
                          print('right')
                  elif GPIO.input(13)==1:
                          q.ChangeDutyCycle(fast)
                          p.ChangeDutyCycle(0)
                          a.ChangeDutyCycle(0)
                          b.ChangeDutyCycle(fast)
                          setLEDs(0, 0, 1, 1)
                          print('left')
except KeyboardInterrupt:
       finished = True  # stop other loops
       GPIO.cleanup()
       sys.exit()
