# -*- coding: utf-8 -*-
"""
High-level API.

"""

import struct

from tsip.config import *
from tsip.llapi import *
from tsip.structs import *

class Packet(object):
    """
    TSIP packet.

    Check the TSIP reference documentation for the description of individual
    packets.

    Examples::

      >>> pkt = Packet(0x1f)                        # Request software versions.
      
      >>> pkt = Packet(0x1e, 0x4b)                  # Request cold-start.
      
      >>> pkt = Packet(0x23, -37.1, 144.1, 10.0)    # Set initial position.
      
      >>> pkt = Packet(0x8e, 0x4f, 0.1)             # Set PPS with to 0.1s

    """

    code = None
    """The code of the packet. This is always 1 byte, 0x8e or 0x8f with "super-packets"."""

    fields = []
    """The data fields of the packet."""


    def __init__(self, code, *args, **kwargs):

        self.code = code

        if self.code in PACKETS_WITH_SUBCODE:
            self.subcode = args[0]
            self.fields = args[1:]
        else:
            self.subcode = None
            self.fields = args


    # The subcode can only be set on TSIP packets that do actually
    # have a subcode. These include all super-packets (0x8e, 0x8f)
    # and a small number of other packets.
    #
    def _set_subcode(self, subcode):
        if subcode is None or self.code in PACKETS_WITH_SUBCODE:
            self._subcode = subcode
        else:
            raise ValueError('Packet %x does not have a sub-code')

    def _get_subcode(self):
        return self._subcode

    subcode = property(_get_subcode, _set_subcode)
    
    
    def _set_fields(self, fields):
        self._fields = list(fields)
    
    def _get_fields(self):
        return self._fields
    
    fields = property(_get_fields, _set_fields)


    def pack(self):
        """Return binary format of packet.

           The returned string is the binary format of the packet. Neither
           stuffing nor framing has been applied.

        """
        
        structs_ = get_structs(self.code, self.subcode)

        for struct_ in structs_:
            try:
                if self.subcode:
                    return struct.pack('>BB', self.code, self.subcode) + struct_.pack(*self.fields)
                else:
                    return struct.pack('>B', self.code) + struct_.pack(*self.fields)
            except struct.error:
                pass
            
        raise ValueError('unable to pack packet')


    @classmethod
    def unpack(cls, packet):
        """Instantiate `Packet` from binary string.

           :param packet: TSIP packet in binary format.
           :type packet: String.

           `packet` must already have framing (DLE...DLE/ETX) removed and
           byte stuffing reversed.

        """

        # The packet must have leading DLE and trailing DLE/ETX removed already!
        # 
        if is_framed(packet):
            raise ValueError('packet contains leading DLE and trailing DLE/ETX')


        # Extract packet code and potential(!) subcode.
        #
        code = struct.unpack('>B', packet[0])[0]
        if code in PACKETS_WITH_SUBCODE:
            subcode = struct.unpack('>B', packet[1])[0]
        else:
            subcode = None
            
            
        structs_ = get_structs(code, subcode)

        
        for struct_ in structs_:
            try:
                if subcode:
                    return cls(code, subcode, *struct_.unpack(packet[2:]))
                else:
                    return cls(code, *struct_.unpack(packet[1:]))
            except struct.error:
                pass
            
        raise ValueError('unable to unpack packet')


    def __repr__(self):
        if self.subcode:
            return 'Packet_%02x/%02x' % (self.code, self.subcode) + str(self.fields)
        else:
            return 'Packet_%02x' % (self.code) + str(self.fields)
 
    

class GPS(gps):

    def __init__(self, reader):
        super(GPS,self).__init__(reader)


    def read(self):
        packet = super(GPS, self).read()

        

        return packet