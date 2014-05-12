import sys, time
import pi2go

pi2go.init()

fast = 40
slow = 30

try:
       while True:
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
