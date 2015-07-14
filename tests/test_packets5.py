# -*- coding: utf-8 -*-

"""
Tests for TSIP packets in the 0x5? range.

* 0x55 - I/O Options report.
* 0x56 - Velocity Fix, East-North-Up (ENU) report.
* 0x57 - Information About Last Computed Fix report.
* 0x58 - Satellite System Data/Acknowledge from Receiver.
* 0x5a - Raw Measurement Data report.
* 0x5c - Satellite Tracking Status report.
* 0x5f - Diagnostics.

"""

from nose.tools import *
from types import *
from tsip import GPS



class Base(object):
    def setup(self):
        self.gps = GPS(open('tests/copernicus2.tsip'))



class Test_5(Base):

    @timed(2.0)
    def test_report_5f(self):
        """0x5f - Diagnostics"""

        while True:
            packet = self.gps.read()

            if packet.code == 0x5f:
                assert len(packet) == 1
                assert isinstance(packet[0], StringType)

                return

