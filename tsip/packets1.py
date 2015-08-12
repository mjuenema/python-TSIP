# -*- coding: utf-8 -*-

"""
TSIP packets in the 0x1? range.

* 0x1c - Version Information command and report.
* 0x1e - Clear Battery Backup, then Reset command.
* 0x1f - Request Software Versions command.

"""

import struct
import collections

from tsip.base import Command, Report, _RO, _RW, _extract_code_from_raw


class Command_1c(Command):
    """
    Version Information.

    :param subcode: The subcode can be ``1`` (firmware version) or ``3`` (hardware version).

    """

    _default = collections.deque([0x1c, 0x1], 2)
    _struct = struct.Struct('>BB')


    def __init__(self, subcode):
        if subcode not in [0x1, 0x3]:
            raise ValueError('invalid sub-code')

        super(Command_1c, self).__init__(subcode)

    subcode = _RW(1)


class Report_1c(Report):
    """
    Version information.

    Report packet 0x1c is sent in reply to command packet 0x1c
    requesting version information. There are two variants of
    this packet, depending on the subcode sent in the command 
    packet. Sub-code 81 reports firmware version information,
    sub-code reports hardware version information.

    """

    _format_81 = struct.Struct('>BBBBBBBBHp')
    _format_83 = struct.Struct('>BBIBBHBHp')

    def __init__(self, raw):

        for _struct in [self._format_81, self._format_83]:
            try:
                self._values = _struct.unpack(raw)
                self._struct = _struct
            except struct.error:
                pass

        if self._values is None:
            raise struct.error('unable to unpack raw packet')

        if self.values[1] not in [0x81, 0x83]:
            raise ValueError('invalid sub-code')

    subcode = _RO(1)

    
class Command_1e(Command):
    """
    Clear Battery Backup, then Reset command.

    """

    _default = collections.deque([0x1e, 0x4b], 2)
    _struct = struct.Struct('>BB')


    def __init__(self, mode):
        if mode not in [0x4b, 0x46, 0x4d]:
            raise ValueError('invalid sub-code')

        super(Command_1e, self).__init__(mode)

    mode = _RW(1)


class Command_1f(Command):
    """
     Request Software Versions command.

    """

    _default = collections.deque([0x1f], 1)
    _struct = struct.Struct('>B')

