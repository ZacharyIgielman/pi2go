import time
import pi2go

pi2go.init()

fast=50
slow=30

while True:
	if pi2go.getDistance()>10:
		pi2go.forward(fast)
	else:
		pi2go.reverse(slow)
		time.sleep(0.5)
		pi2go.stop()
		pi2go.turnReverse(slow,fast)
pi2go.cleanup()
