# -*- coding: utf-8 -*-

"""


"""

import bitstring

import logging
_LOG = logging.getLogger(__name__)


DLE = 0x10
ETX = 0x03

PI = 3.1415926535898	# according to CD-GPS-200 


def _Packet(object):
    pass


def Report(_Packet):
    """

    :param raw: The full TSIP packet in bytes, including leading
                DLE and trailing DLE, ETX.

    """

    def __init__(self, raw):
        self.raw = bitstring.ConstBitStream(bytes=raw)

        # Verify that the first byte is DLE
        #
        dle = self.raw.read('uintbe:8')
        if dle != DLE: 
            raise ValueError('Packet not starting with DLE(0x10)')

        # Read the packet id. In case of TSIP superpackets
        # the ID is two-bytes long. Packet 0x1c has a cub-code.
        #
        if self.raw.peek(8) in [0x8e, 0x8f, 0x1c]:
            self.id = self.raw.read('uintbe:16')
        else:
            self.id = self.raw.read('uintbe:8')


        # Find the right TSIP packet information.
        #
        try:
            self._fmt, self._attrs, _doc = _PACKETS[self.id]
        except KeyError:
            # No packet parser available for this ID
            self._fmt = self._attrs = _doc = None


        # Parse the raw data into fields.
        #
        if self._fmt:
            self._fields = self.raw.unpack(self._fmt)
        else:
            self._fields = None


    def __getitem__(self, i):
        return self._fields[i]
    




