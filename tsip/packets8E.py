# -*- coding: utf-8 -*-

"""
TSIP super-packet commands (0x8e??)

* 0x8e15 - Request current Datum values command.
* 0x8e26 - Write Configuration to NVS command.
* 0x8e41 - Request Manufacturing Paramaters command.
* 0x8e42 - Stored Production Parameters command.
* 0x8e45 - Revert Configuration Segment to Default Settings and Write to NVS command.
* 0x8e4a - Set PPS Characteristics.
* 0x8e4c - Write Configuration Segment to NVS command.
* 0x8e4e - Set PPS output option command.
* 0x8ea0 - Set DAC Value command.
* 0x8ea2 - UTC/GPS Timing command.
* 0x8ea3 - Issue Oscillator Disciplining command.
* 0x8ea5 - Packet Broadcast Mask command.
* 0x8ea6 - Self-Survey command.
* 0x8ea8 - Request Disciplining Parameters command.
* 0x8ea9 - Self-Survey Parameters command.
* 0x8eab - Request Primary Timing Packet command.
* 0x8eac - Request Supplementary Timing Packet command.

"""

import struct

from tsip.constants import *

from tsip.base import *


class Command_8e15(_Command):
    """
    Request current Datum values command

    """

    _format = ''
    _values = []


class Command_8e26(_Command):
    """
    Write Configuration to NVS command

    """

    _format = ''
    _values = []


class Command_8e41(_Command):
    """
    Request Manufacturing Paramaters command

    """

    _format = ''
    _values = []


class Command_8e42(_Command):
    """
    Stored Production Parameters command

    """

    _format = ''
    _values = []


class Command_8e45(_Command):
    """
    Revert Configuration Segment to Default Settings and Write to NVS command

    """

    _format = '>B'
    _values = []


class Command_8e4a(_Command):
    """
    Set PPS Characteristics

    """

    _format = '>BBBdI'
    _values = []


class Command_8e4c(_Command):
    """
    Write Configuration Segment to NVS command

    """

    _format = '>B'
    _values = []


class Command_8e4e(_Command):
    """
    Set PPS output option command

    """

    _format = '>B'
    _values = []


class Command_8ea0(_Command):
    """
    Set DAC Value command

    """

    _format = '>?????'
    _values = []


class Command_8ea2(_Command):
    """
    UTC/GPS Timing command

    """

    _format = '>B'
    _values = []


class Command_8ea3(_Command):
    """
     Issue Oscillator Disciplining command

    """

    _format = '>B'
    _values = []


class Command_8ea5(_Command):
    """
    Packet Broadcast Mask command

    """

    _format = '>HH'
    _values = []


class Command_8ea6(_Command):
    """
    Self-Survey command

    """

    _format = '>B'
    _values = []


class Command_8ea8(_Command):
    """
    Request Disciplining Parameters command

    """

    _format = '>B'
    _values = []


class Command_8ea9(_Command):
    """
    Self-Survey Parameters command

    """

    _format = '>BBII'
    _values = []


class Command_8eab(_Command):
    """
    Request Primary Timing Packet command

    """

    _format = '>B'
    _values = []


class Command_8eac(_Command):
    """
    Request Supplementary Timing Packet command

    """

    _format = '>B'
    _values = []
