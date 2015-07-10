"""


"""

DEVICE = '/dev/ttyAMA0'
SPEED = 38400

from nose.tools import *

import serial
import tsip.gps 
import types


CONN = None
GPS = None


def setup():
    global CONN
    global GPS

    CONN = serial.Serial(DEVICE, SPEED)
    GPS = tsip.gps.GPS(CONN)


def test_read():

    for i in xrange(0, 4):
        packet = GPS.read()

        if packet.code == 0x41:
            assert isinstance(packet[0], types.FloatType)
            assert 0.0 <= packet[0] <= 604801.0

            assert isinstance(packet[1], types.IntType)
            assert packet[1] >= 1851

            assert isinstance(packet[2], types.FloatType)
            assert 14 < packet[2] < 20

          
