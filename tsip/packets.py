# -*- coding: utf-8 -*-

"""
TSIP packets.

This module imports the classes defined in ``packetsN.py`` into
this namespace. 

In addition it defiens the two sepcial packets for TSIP errors 
and Trimble disgnostics (0x5f).


"""

import struct

from tsip.constants import DLE, ETX, PI

from tsip.globals import _PACKET_MAP

from tsip.base import _extract_code_from_raw, register_packet

from tsip.base import Command, Report

from packets1 import Packet_0x1c01
#Command_1c, Report_1c, Command_1e, Command_1f

from packets2 import Command_21, Command_23, Command_24, Command_25, Command_26
from packets2 import Command_27, Command_2b, Command_2d, Command_2e

from packets3 import Command_31, Command_32, Command_35, Command_37, Command_38
from packets3 import Command_3a, Command_3c

from packets4 import Report_41, Report_42, Report_43, Report_45, Report_46, Report_47
from packets4 import Report_4a, Report_4b, Report_4d, Report_4e

from packets5 import Report_55, Report_56, Report_57, Report_58, Report_5a, Report_5c

from packets6 import Report_69, Report_6d

from packets8 import Report_82, Report_83, Report_84, Report_89

from packetsB import Command_bb, Command_bc

from packets8E import Command_8e15, Command_8e26, Command_8e41, Command_8e42, Command_8e45
from packets8E import Command_8e4a, Command_8e4c, Command_8e4e, Command_8ea0, Command_8ea2
from packets8E import Command_8ea3, Command_8ea5, Command_8ea6, Command_8ea8, Command_8ea9
from packets8E import Command_8eab, Command_8eac

from packets8F import Report_8f15, Report_8f17, Report_8f18, Report_8f20, Report_8f21
from packets8F import Report_8f23, Report_8f26, Report_8f2a, Report_8f2b, Report_8f4a
from packets8F import Report_8f4f, Report_8fab,Report_8fac



class Error(Report):
    """
    Parsing error

    """

    _format = '<function parse_0x13 at 0x7f4b8b8cb668>'
    _values = []


class Diagnostics(Report):
    """
    For Trimble diagnostic use only (0x5f)!

    =====   ===============================================
    Index   Description
    =====   ===============================================
    0       The raw diagnostics packet.
    =====   ===============================================


    """

    @property
    def values(self):
        return [self.data]


#_PACKET_MAP = {
#        0x1e: Error,
#	#0x1c: Report_1c,
#	0x41: Report_41,
#	0x42: Report_42,
#	0x43: Report_43,
#	0x45: Report_45,
#	0x46: Report_46,
#	0x47: Report_47,
#	0x4a: Report_4a,
#	0x4b: Report_4b,
#	0x4d: Report_4d,
#	0x4e: Report_4e,
#	0x56: Report_56,
#	0x5c: Report_5c,
#	0x5f: Diagnostics,
#	0x69: Report_69,
#	0x6d: Report_6d,
#	0x82: Report_82,
#	0x83: Report_83,
#	0x84: Report_84,
#	0x89: Report_89,
#	0x8f15: Report_8f15,
#	0x8f17: Report_8f17,
#	0x8f18: Report_8f18,
#	0x8f21: Report_8f21,
#	0x8f23: Report_8f23,
#	0x8f26: Report_8f26,
#	0x8f4f: Report_8f4f,
#	0x8fab: Report_8fab
#}
#"""Map the code of a TSIP report packet to the Python class."""

_code_report_map = _PACKET_MAP


def register_packet(code, cls):
    """
    Register a packet.

    """

    global _PACKET_MAP

    _PACKET_MAP[code] = cls


def _instantiate_report_packet(raw):
    """
    Return an instance of a Report packet class for `code`.

    """

    code = _extract_code_from_raw(raw)
    cls = _code_report_map.get(code)
    if cls is not None:
        try:
            return cls.parse(raw)
        except AttributeError:	# TODO: possibly remove this later
            return None
    else:
        return None
