# -*- coding: utf-8 -*-

"""
Base classes for all TSIP packets

"""

import struct

from tsip.constants import DLE, DLE_STRUCT, ETX, ETX_STRUCT


def _extract_code_from_packet(packet):
    code = struct.unpack('>B', packet[0])[0]
    if code in [0x8E, 0x8F, 0xA0, 0xA5]:
        return struct.unpack('>H', packet[0:2])[0]
    return code


def _extract_data_from_packet(packet):
    code = _extract_code_from_packet(packet)
    if code > 255:
        return packet[2:]
    else:
        return packet[1:]


class Packet(object):
    _code = None
    _format = None
    _values = []

    def __getitem__(self, index):
        return self._values[index]

    def __setitem__(self, i, v):
        self._values[i] = v

    def __len__(self):
        return len(self._values)

    def set_packet(self, packet):
        # TODO: strip DLE, DLE+ETX if still present
        self._packet = packet
        code = _extract_code_from_packet(packet)
        if code != self._code:
            raise ValueError('Packet code %X != Report code %X' %
                             (code, self._code))

        self._data = _extract_data_from_packet(packet)

        if self._format and len(self._data) != self._format.size:
            raise ValueError('ID %04X Got %d bytes, expected %d bytes for %s' %
                             (self._code, len(self._data), self._format.size, self._format))

        try:
            self._values = list(self._format.unpack(self._data))
        except AttributeError:
            # assuming GPS data with extended tsip serial, crc at end
            # need better way to deal with this
            serial, crc = struct.unpack('<HI', self.data[-6:])

            self._values = [ord(c) for c in self.data[0:-6]] + [serial, crc]

    def set_values(self, values):
        if len(values) != self._formatlen:
            raise TypeError('%s takes exactly %d arguments (%d given)' %
                            (self._format.format, self._formatlen, len(values)))
        self._values = values
        self._data = self._pack_values()
        self._packet = self._pack_code() + self._data

    @property
    def code(self):
        return self._code

    @property
    def data(self):
        return self._data

    @property
    def values(self):
        return self._values

    def _pack_code(self):
        if self._code > 255:
            return struct.pack('>H', self._code)
        else:
            return struct.pack('>B', self._code)

    def _pack_values(self):
        return self._format.pack(*self._values)

    @property
    def packet(self):
        return self._packet

    @property
    def _formatlen(self):
        """Number of fields in `self._format`."""
        return len(filter(lambda i: i in 'cbB?hHiIlLqQfdspP', self._format.format))


class Report(Packet):

    def __init__(self, packet=None, values=None):
        if packet is not None:
            self.set_packet(packet)
        elif values is not None:
            self.set_values(values)



# TODO: make self._values a descriptor
class Command(Packet):

    def __init__(self, *args, **kwargs):
        if len(args):
            self.set_values(args)
        elif 'packet' in kwargs:
            self.set_packet(kwargs['packet'])
        elif 'values' in kwargs:
            self.set_values(kwargs['values'])
