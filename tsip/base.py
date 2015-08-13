# -*- coding: utf-8 -*-

"""
Base classes for all TSIP packets

"""

import struct
import collections
import copy

from tsip.constants import DLE, DLE_STRUCT, ETX, ETX_STRUCT


SUPERPACKETS = [0x8e, 0x8f]
"""TSIP superpackets have 2-byte IDs."""


def _extract_code_from_raw(raw):
    code = struct.unpack('>B', raw[0])[0]
    if code in SUPERPACKETS:
        return struct.unpack('>H', raw[0:2])[0]
    return code


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
    """Packet code."""

    _values = None
    """The values contained in the TSIP packet."""

    _struct = None
    """Instance of `struct.Struct` describing the binary structure of the TSIP packet including its code."""


    def __init__(self, *values):
        self._values = list(values)


    @classmethod
    def parse(cls, raw):
        inst = cls()
        inst._values = inst._struct.unpack(raw)[1:]


    def __getitem__(self, i):
        return self._values[i]


    def __setitem__(self, i, v):
        self._values[i] = v


    def __len__(self):
        return len(self.values)


    def _pack(self):
        """Generate the binary structure of the TSIP packet."""
        # TODO: DLE padding!!!
        return self._struct.pack(self._code, *self._values)


#    def _unpack(self, raw):
#        """
#        Parse the binary structure of the TSIP packet.
#
#        :param raw: The binary TSIP packet with leading DLE and trailing DLE+ETX stripped.
#        :returns: List of individual fields as defined by `self._struct`. The first item 
#
#        """
#
#        return list(self._struct.unpack(raw))


    @property
    def code(self):
        return self._code

    
    def __len__(self):
        return len(self._values)
    

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
