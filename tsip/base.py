# -*- coding: utf-8 -*-

"""
Base classes for all TSIP packets

"""

import struct

from tsip.constants import DLE, DLE_STRUCT, ETX, ETX_STRUCT


def _extract_code_from_packet(packet):
    code = struct.unpack('>B', packet[0])[0]
    if code in [0x8f, 0x8e]:
        return struct.unpack('>H', packet[0:2])[0]
    return code

def _extract_data_from_packet(packet):
    code = _extract_code_from_packet(packet)
    if code > 255:
        return packet[2:]
    else:
        return packet[1:]


class Packet(object):
    _format = ''
    _values = []

    def __getitem__(self, index):
        return self._values[index]


class Report(Packet):

    def __init__(self, packet):
        # TODO: strip DLE, DLE+ETX if still present
        self._packet = packet

    @property
    def code(self):
        return _extract_code_from_packet(self._packet)

    
    @property
    def data(self):
        return _extract_data_from_packet(self._packet)


    @property
    def values(self):
        return struct.unpack(self._format, self.data)

    def __getitem__(self, i):
        return self.values[i]

    def __len__(self):
        return len(self.values)


class Command(Packet):

    def __init__(self, code, *values):
        self.code = code
        self.values = values


    def _pack_code(self):
        if self.code > 255:
            return struct.pack('>H', self.code)
        else:
            return struct.pack('>B', self.code)


    def _pack_values(self):
        return struct.pack(self._format, self._values)
        

    @property
    def packet(self):
       return self._pack_code() + self._pack_values()
