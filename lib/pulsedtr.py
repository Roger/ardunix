#!/usr/bin/env python
import serial
import time
import sys

def reset(serial_dev):
    ''' reset arduino arduino'''
    ser = serial.Serial(serial_dev)
    ser.setDTR(1)
    time.sleep(0.5)
    ser.setDTR(0)
    ser.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Please specify a port, e.g. %s /dev/ttyUSB0" % sys.argv[0]
        sys.exit(-1)
    reset(sys.argv[1])
