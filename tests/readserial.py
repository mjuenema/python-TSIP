#!/usr/bin/python

import serial
import sys

try:
    fp = open(sys.argv[1], 'w')
except IndexError:
    sys.stdout.write('%s <outfile>\n' % sys.argv[0])
    sys.exit(1)

conn = serial.Serial('/dev/ttyAMA0', 38400)

while True:
    fp.write(conn.read(1))
