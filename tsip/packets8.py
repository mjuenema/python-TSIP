# -*- coding: utf-8 -*-

"""
TSIP packets in the 0x8? range, excluding super-packets.

* 0x8x - SBAS Correction Status report.
* 0x83 - Double-Precision XYZ Position Fix and Bias Information report.
* 0x84 - Double-Precision LLA Position Fix and Bias Information report.
* 0x89 - Receiver Acquisition Sensitivity Mode report.

"""


import struct

from tsip.base import Command, Report


class Report_82(Report):
    """
    SBAS Correction Status report

    =====   ===============================================
    Index   Description
    =====   ===============================================
    0       SBAS bits
    =====   ===============================================

    """

    _format = '>B'
    _values = []


class Report_83(Report):
    """
    Double-Precision XYZ Position Fix and Bias Information report

    """

    _format = '>ddddf'
    _values = []


class Report_84(Report):
    """
    Double-Precision LLA Position Fix and Bias Information report

    """

    _format = '>ddddf'
    _values = []


class Report_89(Report):
    """
    Receiver Acquisition Sensitivity Mode report

    """

    _format = '>BB'
    _values = []
