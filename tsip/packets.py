# -*- coding: utf-8 -*-

"""
TSIP packets.

This module imports the classes defined in ``packets*.py`` into
this namespace simply for convenience.

In addition it defiens the two sepcial packets for TSIP errors 
and Trimble disgnostics (0x5f).


"""


#import struct

from tsip.constants import DLE, ETX, PI

from tsip.globals import _PACKET_MAP

from tsip.base import _extract_code_from_raw

from packets1 import *
from packets2 import *
from packets3 import *
from packets4 import *
from packets5 import *
from packets6 import *
from packets8 import *
from packetsB import *
from packets8E import *
from packets8F import *


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

_code_report_map = _PACKET_MAP  # TODO: obsolete


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
