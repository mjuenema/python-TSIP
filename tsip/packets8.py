# -*- coding: utf-8 -*-

"""
TSIP packets in the 0x8? range, excluding super-packets.

* 0x8x - SBAS Correction Status report.
* 0x83 - Double-Precision XYZ Position Fix and Bias Information report.
* 0x84 - Double-Precision LLA Position Fix and Bias Information report.
* 0x89 - Receiver Acquisition Sensitivity Mode report.

"""


import struct

from tsip.constants import *

from tsip.base import *


class Report_82(_Report):
    """
    SBAS Correction Status report

    """

    _format = '>B'
    _values = []


class Report_83(_Report):
    """
    Double-Precision XYZ Position Fix and Bias Information report

    """

    _format = '>ddddf'
    _values = []


class Report_84(_Report):
    """
    Double-Precision LLA Position Fix and Bias Information report

    """

    _format = '>ddddf'
    _values = []


class Report_89(_Report):
    """
    Receiver Acquisition Sensitivity Mode report

    """

    _format = '>BB'
    _values = []
