import pi2go, threading, time, sys

pi2go.init()

globalDistance=0
globalStop=0
state=0

def updateDistance():
  global globalDistance
  while True:
    globalDistance=pi2go.getDistance()
    time.sleep(0.5)

threading.timer(0.5,updateDistance())

def mainLoop:
  global globalDistance
  global globalStop
  global state
  while True:
    if globalStop==1 or globalDistance<10:
      pi2go.stop()
    else:
      if state==0:
        #slow lf
      elif state==1:
        #fast lf
      elif state==2:
        #sonar navigator using glpobalDistance
      elif state==3:
        #sonar avoider using globalDistance
      elif state==4:
        #ir navigator
        
threading.timer(0.5,mainLoop())

try:
  while True:
    in=raw_input("")
    globalstop=1
    if in=="":
      globalstop=0
      if state==4:
        state=0
      else:
        state=state+1
      if state==0:
        #led colour
      elif state==1:
        #straight
        #led colour
      elif state==2:
        #led colour
      elif state==3:
        #led colour
      else:
        #led colour
    elif in=="w":
      pi2go.staright(60)
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
