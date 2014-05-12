import time
import pi2go

pi2go.init()

fast=50
slow=30

while True:
	if pi2go.irAll()==False:
		pi2go.forward(fast)
		pi2go.setAllLEDs(4095, 4095, 4095)
	else:
		ir=pi2go.irRight()
		pi2go.setAllLEDs(4095, 0, 0)
		pi2go.reverse(slow)
		time.sleep(0.5)
		pi2go.stop()
		if ir:
			pi2go.setAllLEDs(0, 0, 4095)
			pi2go.turnReverse(fast,slow)
			time.sleep(3)
		else:
			pi2go.setAllLEDs(0, 4095, 0)
			pi2go.turnReverse(slow,fast)
			time.sleep(3)
pi2go.cleanup()
