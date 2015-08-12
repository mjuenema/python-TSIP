# -*- coding: utf-8 -*-

"""
Base classes for all TSIP packets

"""

import struct
import collections

from tsip.constants import DLE, DLE_STRUCT, ETX, ETX_STRUCT


def _extract_code_from_raw(raw):
    code = struct.unpack('>B', raw[0])[0]
    if code in [0x8f, 0x8e]:
        return struct.unpack('>H', raw[0:2])[0]
    return code

def _extract_data_from_raw(raw):
    code = _extract_code_from_raw(raw)
    if code > 255:
        return raw[2:]
    else:
        return raw[1:]


class Packet(object):
    """
    Base class for `Command` and `Report` packets.

    """

    _default = None    
    """Defaults for `_values` (instance of `collections.deque`)."""

    _values = None
    """The values contained in the TSIP packet (instance of `collections.deque`)."""

    _struct = None
    """Instance of `struct.Struct` describing the binary structure of the TSIP packet."""

    def __init__(self):
        """
        The constructor must be defined in the derived class.

        """

        raise NotImplemented

    def __getitem__(self, i):
        return self._values[i]


    def __setitem__(self, i, v):
        self._values[i] = v


    def __len__(self):
        return len(self.values)


    def _pack(self):
        """Generate the binary structure of the TSIP packet."""
        # TODO: DLE padding!!!
        return self._struct.pack(*self._values)


    def _unpack(self, raw):
        """
        Parse the binary structure of the TSIP packet.

        :param raw: The binary TSIP packet with leading DLE and trailing DLE+ETX stripped.
        :returns: List of individual fields as defined by `self._struct`.

        """

        return list(self._struct.unpack(raw))


    @property
    def code(self):
        return self._values[0]

    
    def _get_subcode(self):
        """
        Some TSIP packets contain a subcode. Such packets can simply create
        a property pointing to `_get_subcode` and `_set_subcode` if needed::

            subcode = property(_get_subcode)                 # Report packet
            subcode = property(_get_subcode, _set_subcode)   # Command packet

        """
       
        return self._values[1]


    def _set_subcode(self, value):
        self._values[1] = value


    def __len__(self):
        return len(self._values)
    

class Report(Packet):
    """
    TSIP report packet.

    :param raw: The binary TSIP packet with leading DLE and trailing DLE+ETX stripped.
    :type raw: String.

    Derived classes must either set the `_struct` attribute to match the content of 
    the `raw` TSIP packet or implement a custom `__init__()` method. The latter case 
    is necessary if the structure of the TSIP report packet is not fixed. For example, 
    report packet 0x1c has a different structure depending on its subc-code.

    """

    def __init__(self, raw):
        self._values = self._unpack(raw)


    def __setitem__(self, i, v):
        raise AttributeError('Report packets are read-only')


class Command(Packet):
    """
    TSIP command packet.

    :param *values: Values for the individual fields of the TSIP command packet.

    Derived classes must set the `_struct` attribute to match the content of the `raw` TSIP
    packet. The `_default` attribute must contain the Command packet's code as the first
    field. The `_struct` and `_default` attributes must match insofar as `_default` must
    be a valid argument to the `_pack()` method.

    """

    def __init__(self, *values):

        # Initialise with the default then copy the `*values` skipping
        # the packet code.
        #
        self._values = copy.copy(self._default)

        for i, value in enumerate(values):
            try:
                self._values[i+1] = value
            except IndexError:
                raise ValueError('too many arguments')
