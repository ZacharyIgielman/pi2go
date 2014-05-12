import time
import pi2go

pi2go.init()

fast=50
slow=30

while True:
	if pi2go.getDistance()>10:
		pi2go.forward(fast)
		pi2go.setAllLEDs(4095, 4095, 4095)
	else:
		pi2go.setAllLEDs(4095, 0, 0)
		pi2go.reverse(slow)
		time.sleep(0.5)
		pi2go.stop()
		pi2go.turnReverse(slow,fast)
		pi2go.setAllLEDs(0, 4095, 4095)
		time.sleep(3)
pi2go.cleanup()
