#!/usr/bin/python
# readLightSensor.py
# GUI reading of light detectors
# Author : Zachary Igielman

# must use Python 2.7
import smbus
import time
from Tkinter import *
#import Tkinter must start with capital 'T'
# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the PCF8591
address = 0x48
# 0x00 - 0x03 is AIN0 AIN3
# bus.write_byte(address,0x00)



class App:
        
        def __init__(self, master):
            frame = Frame(master)
            frame.pack()
            Label(frame, text="Analog Value = ").grid(row=0, columnspan=2)

            self.result_var = DoubleVar()
            # location to display data in result_var
            Label(frame, textvariable=self.result_var).grid(row=0, column=2)

            button0 = Button(frame, text="AIN0", command=self.read_AIN0)
            button0.grid(row=1, column=0)

            button1 = Button(frame, text="AIN1", command=self.read_AIN1)
            button1.grid(row=1, column=1)

            button2 = Button(frame, text="AIN2", command=self.read_AIN2)
            button2.grid(row=1, column=2)

            button3 = Button(frame, text="AIN3", command=self.read_AIN3)
            button3.grid(row=1, column=3)

            # get value for DA converter
            self.aout_var = DoubleVar()

            Entry(frame, textvariable=self.aout_var).grid(row=2, columnspan=4)
            button4 = Button(frame, text="AOUT", command=self.writeAOUT)
            button4.grid(row=3, columnspan=4)

            
        def read_AIN0(self):
            bus.write_byte(address,0x40)
            bus.read_byte(address) # dummy read to start conversion
            temp = bus.read_byte(address)
            self.result_var.set(temp)
            
            
        def read_AIN1(self):
            bus.write_byte(address,0x41)
            bus.read_byte(address) # dummy read to start conversion
            temp = bus.read_byte(address)
            self.result_var.set(temp)

        def read_AIN2(self):
            bus.write_byte(address,0x42)
            bus.read_byte(address) # dummy read to start conversion
            temp = bus.read_byte(address)
            self.result_var.set(temp)
            

        def read_AIN3(self):
            bus.write_byte(address,0x43)
            bus.read_byte(address) # dummy read to start conversion
            temp = bus.read_byte(address)
            self.result_var.set(temp)


        def writeAOUT(self):
            temp = self.aout_var.get() # move string value to temp
            temp = int(temp) # change string to integer
            # print temp to see on terminal else comment out
            bus.write_byte_data(address, 0x40, temp)
            
      
root = Tk()
root.wm_title("PCF8591T Demo")
app = App(root)
root.geometry("300x120+0+0")
root.mainloop()
