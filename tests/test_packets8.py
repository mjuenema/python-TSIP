# -*- coding: utf-8 -*-

"""
Tests for TSIP packets in the 0x8? range, excluding super-packets.

* 0x82 - SBAS Correction Status report.
* 0x83 - Double-Precision XYZ Position Fix and Bias Information report.
* 0x84 - Double-Precision LLA Position Fix and Bias Information report.
* 0x89 - Receiver Acquisition Sensitivity Mode report.

"""

from nose.tools import *
from types import *
from tsip import GPS
from base import setup_gps



class Base(object):
    def setup(self):
        self.gps = setup_gps()


class Test_8(Base):

    @timed(2.0)
    def test_report_82(self):
        """0x82 - SBAS Correction Status report"""

        while True:
            packet = self.gps.read()

            if packet.code == 0x82:
                assert len(packet) == 1

                assert isinstance(packet[0], IntType)

                return
