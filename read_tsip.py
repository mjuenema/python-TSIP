#!/usr/bin/env python

"""
Read TSIP from a device of file.

(c) Markus Juenemann, 2015

"""

import sys
import os.path
import serial
import tsip
import time
import binascii


def help():
    sys.stderr.write("%s <file|device> [<baudrate>]\n")
    sys.exit(1)


def main():

    try:
        source = sys.argv[1]
    except IndexError:
        help()


    if os.path.isfile(source):
        conn = open(source)
    else:
        try:
            baud = int(sys.argv[2])
        except IndexError:
            baud = 9600
        except TypeError:
            help()

        conn = serial.Serial(source ,baud)

    gps = tsip.GPS(conn)
      

    for i in xrange(0, 100):
        packet = gps.read()

        if packet:
            print "0x%0x %s" % (packet.code, binascii.hexlify(packet.data))
        else:
            print 'None'


if __name__ == '__main__':
    main()

          
