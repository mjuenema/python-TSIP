# -*- coding: utf-8 -*-

"""
TSIP packets in the 0x3? range.

* 0x31 - Accurate Initial Position (XYZ ECEF) command.
* 0x32 - Accurate Initial Position (Latitude, Longitude, Altitude).
* 0x35 - Set Request I/O Options command.
* 0x37 - Request Status and Values of Last Position and Velocity command.
* 0x38 - Request/Load Satellite System Data command.
* 0x3a - Request Last Raw Measurement command.
* 0x3c - Request Current Satellite Tracking Status command.

"""


import struct

from tsip.base import Command, Report


class Command_31(Command):
    """
    Accurate Initial Position (XYZ ECEF) command

    """

    _fmt = '>fff'
    _values = []


class Command_32(Command):
    """
    Accurate Initial Position (Latitude, Longitude, Altitude)

    """

    _fmt = '>fff'
    _values = []


class Command_35(Command):
    """
    Set Request I/O Options command

    """

    _fmt = '>BBBB'
    _values = []


class Command_37(Command):
    """
    Request Status and Values of Last Position and Velocity command

    """

    _fmt = ''
    _values = []


class Command_38(Command):
    """
    Request/Load Satellite System Data command

    """

    _fmt = '>BBB'
    _values = []


class Command_3a(Command):
    """
    Request Last Raw Measurement command

    """

    _fmt = '>B'
    _values = []


class Command_3c(Command):
    """
    Request Current Satellite Tracking Status command

    """

    _fmt = '>B'
    _values = []

