# -*- coding: utf-8 -*-

"""
TSIP super-packet commands (0x8f??)

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

import struct

from tsip.base import _Command, _Report


class Report_8f15(_Report):
    """
    Current Datum Values report

    """

    _format = '>bddddd'
    _values = []


class Report_8f17(_Report):
    """
    UTM Single Precision Output report

    """

    _format = '>chfffff'
    _values = []


class Report_8f18(_Report):
    """
    UTM Double Precision Output report

    """

    _format = '>chddddf'
    _values = []


class Report_8f20(_Report):
    """
    Last Fix with Extra Information report (binary fixed point)

    """

    _format = '>BhhhHiIiBBBBBBh'
    _values = []


class Report_8f21(_Report):
    """
    Request Accuracy Information report

    """

    _format = '>BHHHHhB'
    _values = []


class Report_8f23(_Report):
    """
    Request Last Compact Fix Information report

    """

    _format = '>IHBBIIihhhH'
    _values = []


class Report_8f26(_Report):
    """
    Non-Volatile Memory Status report

    """

    _format = ''
    _values = []


class Report_8f2a(_Report):
    """
    Fix and Channel Tracking Info report (Type 1)

    """

    _format = '<function parse_0x8f2a at 0x7f4b8b832050>'
    _values = []


class Report_8f2b(_Report):
    """
    Fix and Channel Tracking Info report (Type 2)

    """

    _format = '>BBHIiIiiiiBBB'
    _values = []


class Report_8f4a(_Report):
    """
    Copernicus II GPS Receiver Cable Delay and POS Polarity

    """

    _format = '>BBBdI'
    _values = []


class Report_8f4f(_Report):
    """
    Set PPS width report

    """

    _format = ''
    _values = []


class Report_8fab(_Report):
    """
    Primary Timing Packet report

    """

    _format = '>IHhBBBBBBH'
    _values = []


class Report_8fac(_Report):
    """
    Supplemental Timing Packet

    """

    _format = '>BBBIHHBBBBffI'
    _values = []
