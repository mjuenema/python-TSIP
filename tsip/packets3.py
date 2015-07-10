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

from tsip.base import _Command, _Report


class Command_31(_Command):
    """
    Accurate Initial Position (XYZ ECEF) command

    """

    _format = '>fff'
    _values = []


class Command_32(_Command):
    """
    Accurate Initial Position (Latitude, Longitude, Altitude)

    """

    _format = '>fff'
    _values = []


class Command_35(_Command):
    """
    Set Request I/O Options command

    """

    _format = '>BBBB'
    _values = []


class Command_37(_Command):
    """
    Request Status and Values of Last Position and Velocity command

    """

    _format = ''
    _values = []


class Command_38(_Command):
    """
    Request/Load Satellite System Data command

    """

    _format = '>BBB'
    _values = []


class Command_3a(_Command):
    """
    Request Last Raw Measurement command

    """

    _format = '>B'
    _values = []


class Command_3c(_Command):
    """
    Request Current Satellite Tracking Status command

    """

    _format = '>B'
    _values = []

