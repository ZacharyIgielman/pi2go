import pi2go, threading, time, sys

pi2go.init()

globalDistance=0
globalStop=0
state=0

slowspeed = 20
fastspeed = 100

lastleft = 0
lastright = 0

def updateDistance():
  global globalDistance
  while True:
    globalDistance=pi2go.getDistance()
    time.sleep(0.2)

threading.timer(0.2,updateDistance())

def mainLoop:
  global globalDistance, globalStop, state
  while True:
    if globalStop==1 or globalDistance<5:
      pi2go.stop()
    else:
      if state==0:
        if pi2go.irLeftLine() and pi2go.irRightLine():
          pi2go.forward(40)
        elif pi2go.irRightLine()==False:
          pi2go.spinRight(fast)
        elif pi2go.irLeftLine()==False:
          pi2go.spinLeft(fast)
      elif state==1:
        global slowspeed, fastspeed, lastleft, lastright
        left = pi2go.irLeftLine()
        right = pi2go.irRightLine()
        if left==0 and right==0:
          pi2go.stop()
        if left == 0 and lastleft == 1:
          pi2go.turnForward(slowspeed,fastspeed)
        elif right == 0 and lastright == 1:
          pi2go.turnForward(fastspeed,slowspeed)
        lastleft = left
        lastright = right
        time.sleep(0.01)
      elif state==2:
        if globalDistance>15:
		      pi2go.forward(50)
	      else:
		      pi2go.reverse(30)
		      time.sleep(0.5)
		      pi2go.turnReverse(30,50)
		      time.sleep(3)
      elif state==3:
        if globalDistance>15:
		      pi2go.forward(50)
	      else:
		      pi2go.spinLeft(50)
      elif state==4:
	      if pi2go.irAll()==False:
		      pi2go.forward(fast)
	      else:
		      ir=pi2go.irRight()
		      pi2go.reverse(slow)
		      time.sleep(0.5)
		      if ir:
			      pi2go.turnReverse(50,30)
		      else:
			      pi2go.turnReverse(30,50)
          time.sleep(3)
        
threading.timer(1,mainLoop())

try:
  while True:
    in=raw_input("")
    globalstop=1
    pi2go.setAllLEDs(4095, 0, 0)
    if in=="":
      globalstop=0
      if state==4:
        state=0
      else:
        state=state+1
      if state==0:
        pi2go.setAllLEDs(0, 4095, 0)
      elif state==1:
        pi2go.straight(60)
        pi2go.setAllLEDs(4095, 4095, 0)
      elif state==2:
        pi2go.setAllLEDs(0, 4095, 4095)
      elif state==3:
        pi2go.setAllLEDs(4095, 0, 4095)
      else:
        pi2go.setAllLEDs(0, 0, 4095)
    elif in=="w":
      pi2go.straight(60)
    elif in=="a":
      pi2go.spinLeft(60)
    elif in=="d":
      pi2go.spinRight(60)
    elif in=="s":
      pi2go.reverse(60)
    else:
      pi2go.stop()
except KeyboardInterrupt:
  pi2go.cleanup()
  sys.exit()
