import time
import pi2go

pi2go.init()

fast=50
slow=30

while True:
	if pi2go.irAll()==False:
		pi2go.forward(fast)
	else:
		pi2go.reverse(slow)
		time.sleep(0.5)
		pi2go.stop()
		if pi2go.irLeft():
			pi2go.turnReverse(slow,fast)
		else:
			pi2go.turnReverse(fast,slow)
pi2go.cleanup()
