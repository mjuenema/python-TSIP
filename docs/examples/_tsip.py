"""
Imported by examples so they can actually be executed.

Running the examples is something I use to verify them. Their
main purpose is to be included in the documentation (see 
docs/packets.rst for details). 

MJ, 25-Nov-2015

"""

import sys ; sys.path.append('../..')

import tsip
import serial    # pySerial (https://pypi.python.org/pypi/pyserial)
serial_conn = serial.Serial('/dev/ttyAMAO', 38400)
gps_conn = tsip.GPS(serial_conn)
