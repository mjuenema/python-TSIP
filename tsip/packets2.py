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

from tsip.base import Command, Report


class Command_21(Command):
    """
     Request Current Time command

    """

    _format = ''
    _values = []


class Command_23(Command):
    """
    Initial Position (XYZ ECEF) command

    """

    _format = '>fff'
    _values = []


class Command_24(Command):
    """
    Request GPS Receiver Position Fix Mode command

    """

    _format = ''
    _values = []


class Command_25(Command):
    """
    Initiate Soft Reset & Self Test command

    """

    _format = ''
    _values = []


class Command_26(Command):
    """
    Request Health command

    """

    _format = ''
    _values = []


class Command_27(Command):
    """
    Request Signal Levels command

    """

    _format = ''
    _values = []


class Command_2b(Command):
    """
    Initial Position (Latitude, Longitude, Altitude)

    """

    _format = '>fff'
    _values = []


class Command_2d(Command):
    """
    Request Oscillator Offset command

    """

    _format = ''
    _values = []


class Command_2e(Command):
    """
    Set GPS time

    """

    _format = '>fh'
    _values = []
