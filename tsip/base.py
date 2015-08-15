# -*- coding: utf-8 -*-

"""
Base classes for all TSIP packets

"""

import struct
import collections
import copy

import namedlist

from tsip.globals import _PACKET_MAP
from tsip.constants import DLE, DLE_STRUCT, ETX, ETX_STRUCT


SUPERPACKETS = [0x8e, 0x8f]
"""TSIP superpackets have 2-byte IDs."""


def _extract_code_from_raw(raw):
    code = struct.unpack('>B', raw[0])[0]
    if code in SUPERPACKETS:
        return struct.unpack('>H', raw[0:2])[0]
    return code


def register_packet(code, cls):
    """
    Register a packet with `_PACKET_MAP`

    """

    global _PACKET_MAP

    _PACKET_MAP[code] = cls



class _RO(object):
    def __init__(self, i):
        self.i = i

    def __get__(self, instance, owner):
        return instance[self.i]

class _RW(_RO):

    def __set__(self, instance, value):
        instance[self.i] = value


class Packet(object):
    """
    Base class for `Command` and `Report` packets.

    """

    _code = None
    _subcode = None
    """Packet code and subcode."""

#    _struct = None
#    """Instance of `struct.Struct` describing the binary structure of the TSIP packet including its code."""

    _format = None
    """Format string for `struct.struct()` call."""

    def pack(self):
        """Generate the binary structure of the TSIP packet."""
        b = struct.pack('>B', self.code)

        if self._subcode:
            b += struct.pack('>B', self.subcode)

        if self._format:
            b += struct.pack(self._format, *self)
            # `self` works because derived classes must also derive
            # from `namedlist.namedlist`.

        # TODO: DLE padding!!!
        return b


    @property
    def code(self):
        return self._code


    @property
    def subcode(self):
        return self._subcode


class Report(Packet):
    # TODO: clean-up later
    pass

class Command(Packet):
    # TODO: clean-up later
    pass
    

#class Report(Packet):
#    """
#    TSIP report packet.
#
#    :param raw: The binary TSIP packet with leading DLE and trailing DLE+ETX stripped.
#    :type raw: String.
#
#    Derived classes must either set the `_struct` attribute to match the content of 
#    the `raw` TSIP packet or implement a custom `__init__()` method. The latter case 
#    is necessary if the structure of the TSIP report packet is not fixed. For example, 
#    report packet 0x1c has a different structure depending on its subc-code.
#
#    """
#
#    def __init__(self, raw=None):
#        # `raw` may be ``None`` for `from_values` to work.
#        if raw:
#            self._values = self._unpack(raw)
#
#
#    @classmethod
#    def from_values(cls, *values):
#        """
#
#        """
#
#        inst = cls()
#        inst._values = list(values)
#        return inst
   

#class Command(Packet):
#    """
#    TSIP command packet.
#
#    :param *values: Values for the individual fields of the TSIP command packet.
#
#    Derived classes must set the `_struct` attribute to match the content of the `raw` TSIP
#    packet. The `_default` attribute must contain the Command packet's code as the first
#    field. The `_struct` and `_default` attributes must match insofar as `_default` must
#    be a valid argument to the `_pack()` method.
#
#    """
#
#    def __init__(self, *values):
#        self._values = list(values)
#
#        # Initialise with the default then copy the `*values`.
#        #
#        self._values = copy.copy(self._default)
#
#        for (i, value) in enumerate(values):
#            try:
#                self._values[i] = value
#            except IndexError:
#                raise ValueError('too many arguments')
