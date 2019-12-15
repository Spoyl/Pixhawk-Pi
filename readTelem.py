# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 22:08:04 2019

@author: Oliver

Script to read data from a 433 SiK radio connected to a laptop via USB
(port may be different on each systems).
"""

import serial

ser = serial.Serial(port="COM14", baudrate=57600, timeout = 5)

while True:
    
    try:
        inp = ser.readline()
        print(inp)
    
    except:
        ser.close()        
        
ser.close()