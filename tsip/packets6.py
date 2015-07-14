# -*- coding: utf-8 -*-

"""
TSIP packets in the 0x6? range.

* 0x69 - Receiver Acquisition Sensitivity Mode report.
* 0x6d - All-In-View Satellite Selection report.

"""


import struct

from tsip.base import Command, Report
from tsip.misc import b012, b3, b4567


class Report_69(Report):
    """
    Receiver Acquisition Sensitivity Mode report

    """

    _format = '>B'
    _values = []


class Report_6d(Report):
    """
    All-In-View Satellite Selection report

    =====   ===============================================
    Index   Description
    =====   ===============================================
    0       Dimension, Auto/Manual, nSVs (byte 0)
    1       PDOP
    2       HDOP
    3       VDOP
    4       TDOP
    5       SV PRN (list): [prn1, prn2, ...]
    =====   ===============================================
    
    In addition to access by field index there are some convenience
    properties to extract the bits from byte 0.
    
    * `Report_6d.dimension` is either 3 (2D) or 4 (3D).
    * `Report_6d.auto_manual` is either 0 (auto) or 1 (manual)
    * `Report_6d.is_manual` is ``
    
    """

    _format = '>Bffff'

    @property
    def dimension(self):
        return b012(self.values[0])
    
    @property
    def auto_manual(self):
        return b3(self.values[0])
    
    @property
    def is_auto(self):
        return self.auto_manual == 0
    
    @property
    def is_manual(self):
        return self.auto_manual == 1
    
    @property
    def nsv(self):
        return len(self.values[5])

    @property
    def values(self):
        (byte0, pdop, hdop, vdop, tdop) = struct.unpack(self._format, self.data[0:17])

        #dimension = b012(byte0)
        #auto = b3(byte0)
        nsv = b4567(byte0)

        prn = []
        for i in xrange(0, nsv):
            prn.append(struct.unpack('>B', self.data[17+i])[0])

        return [byte0, pdop, hdop, vdop, tdop, prn]
