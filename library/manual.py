import pi2go

pi2go.init()

while True:

	key=raw_input("Where do you want to go (W, A, S, D or other)?")

        if key=="d":
		pi2go.setAllLEDs(0, 4095, 0)
                print "right"
                pi2go.spinRight(100)

        elif key=="a":
		pi2go.setAllLEDs(0, 0, 4095)
                print "left"
		pi2go.spinLeft(100)

        elif key=="s":
		pi2go.setAllLEDs(4095, 0, 0)
                print "back"
                pi2go.reverse(100)

        elif key=="w":
		pi2go.setAllLEDs(4095, 4095, 4095)
                print "up"
                pi2go.forward(100)

	else:
		pi2go.setAllLEDs(0, 0, 0)
		pi2go.stop()
