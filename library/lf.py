import sys, time
import pi2go

pi2go.init()

pwmMax = 4095

fast = 40

try:
       while True:
                  if pi2go.irLeftLine() and pi2go.irRightLine():
                          pi2go.forward(fast)
                          pi2go.setAllLEDs(pwmMax, pwmMax, pwmMax)  # Turn LEDs White for Forwards
                          print('straight')
                  elif pi2go.irRightLine()==False:
                          pi2go.spinRight(fast)
                          pi2go.setAllLEDs(pwmMax, 0, 0) # Turn LEDs Red for Right
                          print('right')
                  elif pi2go.irLeftLine()==False:
                          pi2go.spinLeft(fast)
                          pi2go.setAllLEDs(0, 0, pwmMax) # Turn LEDs Blue to Left
                          print('left')
except KeyboardInterrupt:
       pi2go.setAllLEDs (0, 0, 0)
       pi2go.cleanup()
       sys.exit()
