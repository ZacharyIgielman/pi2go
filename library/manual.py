import time
import curses
from sys import exit
import pi2go

pi2go.init()

shell = curses.initscr()
shell.nodelay(False)

while True:
    key = shell.getch()

    if key == 119:
        print("Forward")
        pi2go.forward(100)

    elif key == 115:
        print ("Backward")
        pi2go.reverse(100)    
	   
    elif key == 97:
        print ("Left")
        pi2go.spinLeft(50)

    elif key == 100:
        print ("Right")
        spinRight(50)
      
    if key == 24:
        curses.endwin()
        exit(0)
    time.sleep(0.03)
    pi2go.stop()

pi2go.cleanup()
