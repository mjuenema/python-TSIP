# -*- coding: utf-8 -*-

"""
TSIP packets in the 0x5? range.

* 0x55 - I/O Options report.
* 0x56 - Velocity Fix, East-North-Up (ENU) report.
* 0x57 - Information About Last Computed Fix report.
* 0x58 - Satellite System Data/Acknowledge from Receiver.
* 0x5a - Raw Measurement Data report.
* 0x5c - Satellite Tracking Status report.

"""


import struct

from tsip.constants import *

from tsip.base import *


class Report_55(_Report):
    """
    I/O Options report.

    """

    _format = '>BBBB'
    _values = []


class Report_56(_Report):
    """
    Velocity Fix, East-North-Up (ENU) report

    """

    _format = '>fffff'
    _values = []


class Report_57(_Report):
    """
     Information About Last Computed Fix

    """

    _format = '>BBfh'
    _values = []


class Report_58(_Report):
    """
    Satellite System Data/Acknowledge from Receiver

    """

    _format = '>?????'
    _values = []


class Report_5a(_Report):
    """
    Raw Measurement Data

    """

    _format = '>BBBBBfffd'
    _values = []


class Report_5c(_Report):
    """
    Satellite Tracking Status report

    """

    _format = '>BBBBffffB'
    _values = []
