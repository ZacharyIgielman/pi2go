# Testing PCF8591 ADC Chip

import time
import sys
import RPi.GPIO as gpio
from sgh_PCF8591P import sgh_PCF8591P

pcfSensor = None
try:
    pcfSensor = sgh_PCF8591P(1) #i2c, 0x48)
    print pcfSensor
    print "PCF8591P Detected"
except:
    print "No PCF8591 Detected"
    
while True:
    adc1 = pcfSensor.readADC(0) # get a value
    adc2 = pcfSensor.readADC(1) # get a value
    adc3 = pcfSensor.readADC(2) # get a value
    adc4 = pcfSensor.readADC(3) # get a value
    print'ADC1:',adc1,' ADC2:',adc2,' ADC3:',adc3,' ADC4:',adc4
    time.sleep(1)

