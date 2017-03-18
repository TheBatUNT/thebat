#!/usr/bin/env python2
import serial
ser = serial.Serial('/dev/rfcomm1',9600)

ser.write('1')


