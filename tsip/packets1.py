# -*- coding: utf-8 -*-

"""
TSIP packets in the 0x1? range.

* 0x1c - Version Information command and report.
* 0x1e - Clear Battery Backup, then Reset command.
* 0x1f - Request Software Versions command.

"""

import struct

from tsip.base import Command, Report


class Command_1c(Command):
    """
    Version Information.

    :param subcode: The subcode can be ``1`` (firmware version) or
        ``3`` (hardware version).

    """

    _format = '>B'
    _values = []

    def __init__(self, subcode):
        if subcode not in [1, 3]:
            raise ValueError("subcode must be either 1 or 3")

        super(Command_1c, self).__init__(0x1c, subcode)
        self._values = [subcode]


class Report_1c(Report):
    """
    Version information.

    Report packet 0x1c is sent in reply to command packet 0x1c
    requesting version information. There are two variants of
    this packet, depending on the subcode sent in the command 
    packet. Sub-code 81 reports firmware version information,
    sub-code reports hardware version information.

    """

    _format    = None
    _format_83 = '>BIBBHBHp'
    _format_81 = '>BBBBBBBHp'
    

    def __init__(self, packet):
        super(Report_1c, self).__super__(packet)
        if struct.unpack('>B', packet[1]) == 1:
            self._format == self._format_81
        elif struct.unpack('>B', packet[1]) == 3:
            self._format == self._format_83
        else:
            raise ValueError('sub-code of report packet 0x1c must be 1 or 3')
       

    
# ---  ------------

class Command_1e(Command):
    """
     Clear Battery Backup, then Reset command

    """

    _format = '>B'
    _values = []


class Command_1f(Command):
    """
     Request Software Versions command

    """

    _format = ''
    _values = []

