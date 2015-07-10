# -*- coding: utf-8 -*-

"""
TSIP packets in the 0x4? range.

* 0x41 - GPS Time report.
* 0x42 - Single-Precision Position Fix, XYZ ECEF report.
* 0x43 - Velocity Fix, XYZ ECEF report.
* 0x45 - Software Version Information report.
* 0x46 - Health of Receiver report.
* 0x47 - Signal Levels for all Satellites report.
* 0x4a - Single Precision LLA Position Fix report.
* 0x4b - Machine/ Code ID and Additional Status report.
* 0x4d - Oscillator Offset report.
* 0x4e - Response to Set GPS Time report.

"""


import struct

from tsip.constants import *

from tsip.base import *


class Report_41(_Report):
    """
    GPS Time report

    """

    _format = '>fhf'
    _values = []


class Report_42(_Report):
    """
    Single-Precision Position Fix, XYZ ECEF report

    """

    _format = '>ffff'
    _values = []


class Report_43(_Report):
    """
    Velocity Fix, XYZ ECEF report

    """

    _format = '>fffff'
    _values = []


class Report_45(_Report):
    """
    Software Version Information report

    """

    _format = '>BBBBBBBBBB'
    _values = []


class Report_46(_Report):
    """
    Health of Receiver report

    """

    _format = '>BB'
    _values = []


class Report_47(_Report):
    """
    Signal Levels for all Satellites report

    """

    _format = ''
    _values = []


class Report_4a(_Report):
    """
    Single Precision LLA Position Fix report

    """

    _format = '>fffff'
    _values = []


class Report_4b(_Report):
    """
    Machine/ Code ID and Additional Status report

    """

    _format = '>BBB'
    _values = []


class Report_4d(_Report):
    """
    Oscillator Offset report

    """

    _format = '>f'
    _values = []


class Report_4e(_Report):
    """
    Response to Set GPS Time report

    """

    _format = '>c'
    _values = []

