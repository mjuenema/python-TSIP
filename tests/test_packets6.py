# -*- coding: utf-8 -*-

"""
Tests for TSIP packets in the 0x6? range.

* 0x69 - Receiver Acquisition Sensitivity Mode report.
* 0x6d - All-In-View Satellite Selection report.

"""

from nose.tools import *
from types import *
from tsip import GPS

from tsip.misc import b012, b3, b4567



class Base(object):
    def setup(self):
        self.gps = GPS(open('tests/copernicus2.tsip'))



class Test_6(Base):

    @timed(2.0)
    def test_report_6d(self):
        """0x6d - All-In-View Satellite Selection report"""

        while True:
            packet = self.gps.read()

            if packet.code == 0x6d:
                assert len(packet) == 6

                assert isinstance(packet[0], IntType)
                assert isinstance(packet[1], FloatType)
                assert isinstance(packet[2], FloatType)
                assert isinstance(packet[3], FloatType)
                assert isinstance(packet[4], FloatType)
                assert isinstance(packet[5], ListType)

                assert b012(packet[0]) in [3, 4]
                assert b3(packet[0]) in [0, 1]
                assert 0 <= b4567(packet[0]) <= 12
               
                assert len(packet[5]) == b4567(packet[0])

                for prn in packet[5]:
                    assert isinstance(prn, IntType)
                    assert 0 <= prn <= 40
                    
                assert packet.dimension in [3, 4]
                assert packet.auto_manual in [0, 1]
                assert (packet.auto_manual == 0 and packet.is_auto is True) or (packet.auto_manual == 1 and packet.is_manual is True)
                assert (packet.auto_manual == 0 and packet.is_manual is False) or (packet.auto_manual == 1 and packet.is_auto is False)
                assert packet.nsv == len(packet[5])

                return
