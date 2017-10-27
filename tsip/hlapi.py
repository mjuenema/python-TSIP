# -*- coding: utf-7 -*-
"""
High-level API.

"""

import struct
import binascii

from tsip.config import *
from tsip.llapi import *
from tsip.structs import *


class PackError(Exception):
    def __init__(self, packet):
        self.packet = packet

    def __repr__(self):
        return 'unable to pack packet %s' % (self.packet)


class Packet(object):
    """
    TSIP packet.

    Check the TSIP reference documentation for the description of individual
    packets.

    The argument(s) to `Packet()` can be either individual values, a single
    tuple or a single list.

    Examples::

      >>> pkt = Packet(0x1f)                          # Request software versions.
      >>> pkt = Packet(0x1e, 0x4b)                    # Request cold-start.
      >>> pkt = Packet( (0x23, -37.1, 144.1, 10.0) )  # Set initial position (tuple).
      >>> pkt = Packet( [0x8e, 0x4f, 0.1] )           # Set PPS with to 0.1s (list)

    """

    _fields = []
    """The data fields of the packet."""


    def __init__(self, *fields):

        # Allow `*fields` to be either individual arguments or a list or tuple.
        # Because `fields` will always be a tuple anyway, passing a list or
        # tuple will result in `fields` being a nested structure.A
        #
        # Packet(1,2,3)   -> (1,2,3)   -> self.fields = fields
        # Packet((1,2,3)) -> ((1,2,3)) -> self.fields = fields[0]
        # Packet([1,2,3]) -> [(1,2,3)] -> self.fields = fields[0]
        #
        try:
            fields[0][0]             # Passed list or tuple to `Packet()`?
            self.fields = fields[0]
        except TypeError:
            self.fields = fields

    # Packets are equal if their fields are equal
    #
    def __eq__(self, other):
        return self.fields == other.fields


    # Make self.fields accessible as indexes on the
    # packet instance.
    #
    def __getitem__(self, index):
        return self.fields[index]

    def __setitem__(self, index, value):
        self.fields[index] = value

    def __iter__(self):     # TODO: tests for __iter__
        return iter(self.fields)

    def __len__(self):      # TODO: tests for __len__
        return len(self.fields)

    def _set_fields(self, fields):
        self._fields = list(fields)

    def _get_fields(self):
        return self._fields

    fields = property(_get_fields, _set_fields)


    def pack(self):
        """Return binary format of packet.

           The returned string is the binary format of the packet with
           stuffing and framing applied. It is ready to be sent to
           the GPS.

        """

        # Possible structs for packet ID.
        #
        try:
            structs_ = get_structs_for_fields([self.fields[0]])
        except (TypeError):
            # TypeError, if self.fields[0] is a wrong argument to `chr()`.
            raise PackError(self)


        # Possible structs for packet ID + subcode
        #
        if structs_ == []:
            try:
                structs_ = get_structs_for_fields([self.fields[0], self.fields[1]])
            except (IndexError, TypeError):
                # IndexError, if no self.fields[1]
                # TypeError, if self.fields[1] is a wrong argument to `chr()`.
                raise PackError(self)


        # Try to pack the packet with any of the possible structs.
        #
        for struct_ in structs_:
            try:
                return struct_.pack(*self.fields)
            except struct.error:
                pass

        # We only get here if the ``return`` inside the``for`` loop
        # above wasn't reached, i.e. none of the `structs_` matched.
        #
        raise PackError(self)


    @classmethod
    def unpack(cls, rawpacket):
        """Instantiate `Packet` from binary string.

           :param rawpacket: TSIP pkt in binary format.
           :type rawpacket: String.

           `rawpacket` must already have framing (DLE...DLE/ETX) removed and
           byte stuffing reversed.

        """

        structs_ = get_structs_for_rawpacket(rawpacket)

        for struct_ in structs_:
            try:
                return cls(*struct_.unpack(rawpacket))
            except struct.error:
                raise
                # Try next one.
                pass

        # Packet ID 0xff is a pseudo-packet representing
        # packets unknown to `python-TSIP` in their raw format.
        #
        return cls(0xff, rawpacket)


    def __repr__(self):
        return 'Packet%s' % (str(tuple(self.fields)))


class GPS(gps):

    def __init__(self, conn):
        super(GPS, self).__init__(conn)


    def read(self):
        pkt = super(GPS, self).read()
        return Packet.unpack(unstuff(unframe(pkt)))

    def write(self, packet):
        super(GPS, self).write(frame(stuff(packet.pack())))
