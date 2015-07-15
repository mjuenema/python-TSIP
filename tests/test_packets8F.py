# -*- coding: utf-8 -*-

"""
Tests for TSIP packets in the 0x8f?? range.

* 0x8f15 - Current Datum Values report.
* 0x8f17 - UTM Single Precision Output report.
* 0x8f18 - UTM Double Precision Output report.
* 0x8f20 - Last Fix with Extra Information report.
* 0x8f21 - Request Accuracy Information report.
* 0x8f23 - Request Last Compact Fix Information report.
* 0x8f26 - Non-Volatile Memory Status report.
* 0x8f2a - Fix and Channel Tracking Info report (Type 1).
* 0x8f2b - Fix and Channel Tracking Info report (Type 2).
* 0x8f4a - Copernicus II GPS Receiver Cable Delay and POS Polarity.
* 0x8f4f - Set PPS width report.
* 0x8fab - Primary Timing Packet report.
* 0x8fac - Supplemental Timing Packet.

"""

import datetime

from nose.tools import *
from types import *
from serial import Serial
from tsip import GPS



class Base(object):
    def setup(self):
        self.gps = GPS(Serial('/dev/ttyAMA0', 38400))



class Test_8f(Base):

    @timed(2)
    def test_report_8f23(self):
        """0x8f23 - Request Last Compact Fix Information report"""

        while True:
            packet = self.gps.read()

            if packet.code == 0x8f23:
                assert len(packet) == 11

                assert isinstance(packet[0], IntType)
                assert isinstance(packet[1], IntType)
                assert isinstance(packet[2], IntType)
                assert isinstance(packet[3], IntType)
                assert isinstance(packet[4], IntType)
                assert isinstance(packet[5], IntType)
                assert isinstance(packet[6], IntType)
                assert isinstance(packet[7], IntType)
                assert isinstance(packet[8], IntType)
                assert isinstance(packet[9], IntType)
                assert isinstance(packet[10], IntType)
                
                assert isinstance(packet.utc_datetime, datetime.datetime)
                assert isinstance(packet.gps_datetime, datetime.datetime)
                assert isinstance(packet.fix_time, FloatType)
                assert isinstance(packet.week_number, IntType)
                assert isinstance(packet.leap_second_offset, IntType)
                assert isinstance(packet.longitude, FloatType)
                assert isinstance(packet.latitude, FloatType)
                assert isinstance(packet.altitude, FloatType)
                assert isinstance(packet.velocity_scale, FloatType)
                assert isinstance(packet.fix_available, BooleanType)
                assert isinstance(packet.dgps, BooleanType)
                assert isinstance(packet.two_d, BooleanType)
                
                assert 0.0 <= packet.fix_time <= 604800000.0
                assert packet.week_number >= 1851
                assert packet.leap_second_offset >= 17 
                assert -90.0 <= packet.latitude <= 90.0
                assert 0.0 <= packet.longitude <= 180.0
                assert -100.0 <= packet.altitude <= 10000.0
                assert packet.velocity_scale in [0.002, 0.005]

                return
