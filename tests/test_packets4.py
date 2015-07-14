# -*- coding: utf-8 -*-

"""
Tests for TSIP packets in the 0x4? range.

* 0x41 - GPS Time report.
* 0x42 - Single-Precision Position Fix, XYZ ECEF report.
* 0x43 - Velocity Fix, XYZ ECEF report.
* 0x45 - Software Version Information report.
* 0x46 - Health of Receiver report.
* 0x47 - Signal Levels for all Satellites report.
* 0x4a - Single Precision LLA Position Fix report.
* 0x4b - Machine/Code ID and Additional Status report.
* 0x4d - Oscillator Offset report.
* 0x4e - Response to Set GPS Time report.

"""

from nose.tools import *
from types import *
from tsip import GPS



class Base(object):
    def setup(self):
        self.gps = GPS(open('tests/copernicus2.tsip'))



class Test_4(Base):

    @timed(2.0)
    def test_report_41(self):
        """0x41 - GPS Time report"""

        while True:
            packet = self.gps.read()

            if packet.code == 0x41:
                assert len(packet) == 3

                assert isinstance(packet[0], FloatType)
                assert isinstance(packet[1], IntType)
                assert isinstance(packet[2], FloatType)

                assert 0.0 <= packet[0] <= 604801.0
                assert packet[1] >= 1851
                assert packet[2] >= 17.0	# post 01-July-2015

                return


    @timed(2.0)
    def test_report_46(self):
        """0x46 - Health of Receiver report"""

        while True:
            packet = self.gps.read()

            if packet.code == 0x46:
                assert len(packet) == 2

                assert isinstance(packet[0], IntType)
                assert isinstance(packet[1], IntType)

                return


    @timed(2.0)
    def test_report_4b(self):
        """0x4b - Machine/Code ID and Additional Status report"""

        while True:
            packet = self.gps.read()

            if packet.code == 0x4b:
                assert len(packet) == 3

                assert isinstance(packet[0], IntType)
                assert isinstance(packet[1], IntType)
                assert isinstance(packet[2], IntType)

                return
