import pi2go, threading, time, sys

pi2go.init()

globalDistance=0
globalStop=0
state=0

slowspeed = 20
fastspeed = 100

lastleft = 0
lastright = 0

finished = False

def updateDistance():
  global globalDistance, finished
  while finished == False:
    globalDistance=pi2go.getDistance()
    time.sleep(0.2)

threading.Thread(target = updateDistance).start()

def mainLoop():
  global globalDistance, globalStop, state, finished
  global slowspeed, fastspeed, lastleft, lastright
  while finished == False:
    if globalStop==1 or globalDistance<5:
      pi2go.stop()
    else:
      if state==0:  # Standard Line Follower
        if pi2go.irLeftLine() and pi2go.irRightLine():
          pi2go.forward(40)
        elif pi2go.irRightLine()==False:
          pi2go.spinRight(fastspeed)
        elif pi2go.irLeftLine()==False:
          pi2go.spinLeft(fastspeed)

      elif state==1:  # Fast Line Follower
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

      elif state==2:  # Obstacle avoider (reverses then spins when near object)
        if globalDistance>15:
          pi2go.forward(50)
        else:
          pi2go.reverse(30)
          time.sleep(0.5)
          pi2go.turnReverse(30,50)
          time.sleep(3)

      elif state==3:  # Obstacle avoider (spins when near object)
        if globalDistance>15:
          pi2go.forward(50)
        else:
          pi2go.spinLeft(50)

      elif state==4:  # Avoids objects using IR sensors only
        if pi2go.irAll()==False:
          pi2go.forward(50)
        else:
          ir=pi2go.irRight()
          pi2go.reverse(30)
          time.sleep(0.5)
          if ir:
            pi2go.turnReverse(50,30)
          else:
            pi2go.turnReverse(30,50)
          time.sleep(3)
        
threading.Thread(target = mainLoop).start()

try:
  while True:
    inp = raw_input("}}")
    globalstop=1
    pi2go.setAllLEDs(4095, 0, 0)
    if inp=="":
      globalstop=0
      if state==4:
        state=0
      else:
        state=state+1
      if state==0:
        pi2go.setAllLEDs(0, 4095, 0)
      elif state==1:
        pi2go.forward(60)
        pi2go.setAllLEDs(4095, 4095, 0)
      elif state==2:
        pi2go.setAllLEDs(0, 4095, 4095)
      elif state==3:
        pi2go.setAllLEDs(4095, 0, 4095)
      else:
        pi2go.setAllLEDs(0, 0, 4095)
    elif inp=="w":
      pi2go.forward(60)
    elif inp=="a":
      pi2go.spinLeft(60)
    elif inp=="d":
      pi2go.spinRight(60)
    elif inp=="s":
      pi2go.reverse(60)
    else:
      pi2go.stop()

except KeyboardInterrupt:
#except:
  finished = True
  time.sleep(1) # wait for threads to finish
  pi2go.cleanup()
  sys.exit()
