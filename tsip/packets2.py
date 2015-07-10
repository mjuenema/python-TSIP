# -*- coding: utf-8 -*-

"""
TSIP packets in the 0x2? range.

* 0x21 - Request Current Time command.
* 0x23 - Initial Position (XYZ ECEF) command.
* 0x24 - Request GPS Receiver Position Fix Mode command.
* 0x25 - Initiate Soft Reset & Self Test command.
* 0x26 - Request Health command.
* 0x27 - Request Signal Levels command.
* 0x2b - Initial Position (Latitude, Longitude, Altitude) command.
* 0x2d - Request Oscillator Offset command.
* 0x2e - Set GPS time command.

"""


import struct

from tsip.base import _Command, _Report


class Command_21(_Command):
    """
     Request Current Time command

    """

    _format = ''
    _values = []


class Command_23(_Command):
    """
    Initial Position (XYZ ECEF) command

    """

    _format = '>fff'
    _values = []


class Command_24(_Command):
    """
    Request GPS Receiver Position Fix Mode command

    """

    _format = ''
    _values = []


class Command_25(_Command):
    """
    Initiate Soft Reset & Self Test command

    """

    _format = ''
    _values = []


class Command_26(_Command):
    """
    Request Health command

    """

    _format = ''
    _values = []


class Command_27(_Command):
    """
    Request Signal Levels command

    """

    _format = ''
    _values = []


class Command_2b(_Command):
    """
    Initial Position (Latitude, Longitude, Altitude)

    """

    _format = '>fff'
    _values = []


class Command_2d(_Command):
    """
    Request Oscillator Offset command

    """

    _format = ''
    _values = []


class Command_2e(_Command):
    """
    Set GPS time

    """

    _format = '>fh'
    _values = []
