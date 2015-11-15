#!/usr/bin/python

from binascii import hexlify
import struct

# DLE and ETX as values
#
DLE = 0x10
ETX = 0x03


# DLE and ETX as characters
#
CHR_DLE = chr(DLE)
CHR_ETX = chr(ETX)


# List of packets which have a sub-code.
#
#PACKETS_WITH_SUBCODE = [0x8e, 0x8f, 0x1c, 0x7a, 0x7e, 0xbb]
PACKETS_WITH_SUBCODE = [0x1c, 0x7a, 0x7e, 0xbb]


# Packet structures.
#
# Packets with sub-codes are two tiered: [code][subcode].
#
PACKET_STRUCTURES = {
    # Command Packet 0x1C - Firmware Version
    0x1c: { 0x01: None,
    # Report Packet 0x1C - Firmware Version
            0x81: struct.Struct('>BBBBBBHBB'),
    # Command Packet 0x1C - Hardware Component Version Information
            0x03: None,
    # Report Packet 0x1C - Hardware Component Version Information
            0x83: struct.Struct('>IBBHBHp') },
    # Command Packet 0x1E - Clear Battery Backup, then Reset
    0x1e: struct.Struct('>B'),
    # Command Packet 0x1F - Request Software Versions
    0x1f: None,
    # Command Packet 0x21 - Request Current Time
    0x21: None,
    # Command Packet 0x23 - Initial Position (XYZ ECEF)
    0x23: struct.Struct('>fff'),
}


def is_framed(packet):
    """
    Check whether a packet contains leading DLE and trailing DLE/ETX.

    :param packet: TSIP packet with or without leading DLE and trailing DLE/ETX.
    :type packet: Binary string.
    :returns: ``True`` if leading DLE and trailing DLE/ETX are still present,
        ``False`` otherwise.

    """

    return packet[0] == CHR_DLE and packet[-2] == CHR_DLE and packet[-1] == CHR_ETX


def frame(packet):
    """
    Add leading DLE and trailing DLE/ETX to packet. 

    :param packet: TSIP packet without leading DLE and trailing DLE/ETX.
    :type packet: Binary string.
    :return: TSIP packet with leading DLE and trailing DLE/ETX added.

    If the packet already starts with DLE and ends in DLE/ETX then the 
    packet is returned unchanged.

    """

    if is_framed(packet):
        return packet
    else:
        return CHR_DLE + packet + CHR_DLE + CHR_ETX


def unframe(packet):
    """
    Strip leading DLE and trailing DLE/ETX from packet. 

    :param packet: TSIP packet with leading DLE and trailing DLE/ETX.
    :type packet: Binary string.
    :return: TSIP packet with leading DLE and trailing DLE/ETX removed.

    If the packet does not start with DLE _and_ end with DLE/ETX it will be
    returned unchanged. It should therefore be reasonably safe to "strip" a
    packet twice. A packet must be stripped first before it is "unstuffed".

    The `frame()` function is the opposite to `strip()`. 

    """

    if is_framed(packet):
        return packet.lstrip(CHR_DLE).rstrip(CHR_ETX).rstrip(CHR_DLE)
    else:
        return packet


def stuff(packet):
    """
    Add byte stuffing to TSIP packet.
    :param packet: TSIP packet with byte stuffing. The packet must already
        have been stripped or `ValueError` will be raised.
    :type packet: Binary string.
    :return: Packet with byte stuffing.

    """

    if is_framed(packet):
        return packet.replace(CHR_DLE + CHR_DLE, CHR_DLE)
    else:
        raise ValueError('packet contains leading DLE and trailing DLE/ETX')


def unstuff(packet):
    """
    Remove byte stuffing from a TSIP packet.

    :param packet: TSIP packet with byte stuffing. The packet must already
        have been stripped or `ValueError` will be raised.
    :type packet: Binary string.
    :return: Packet without byte stuffing.

    """

    if is_framed(packet):
        raise ValueError('packet contains leading DLE and trailing DLE/ETX')
    else:
        return packet.replace(CHR_DLE + CHR_DLE, CHR_DLE)


class gps(object):

    def __init__(self, reader):
        self.reader = reader

    def __iter__(self):
        return self

    def read(self):
    
        packet = ''
        dle_count = 0

        while True:
            b = self.reader.read(1)

            if b == '':
                return None

            packet += b

            if b == CHR_DLE:
                dle_count += 1
            elif b == CHR_ETX and (dle_count % 2) == 0:    # even, because leading DLE is counted!
                return unstuff(unframe(packet))
                packet = ''
                dle_count = 0
            else:
                pass


    def next(self):
        packet = self.read()

        if packet is None:
            raise StopIteration()
        else:
            return packet


class Packet(object):
    """
    TSIP packet.

    Check the TSIP reference documentation for the description of individual
    packets.

    Examples::

      >>> pkt = Packet(0x1f)                        # Request software versions.
      
      >>> pkt = Packet(0x1e, 0x4b)                  # Request cold-start.
      >>> pkt = Packet(0x1e4b)                      # Request cold-start.
      
      >>> pkt = Packet(0x23, -37.1, 144.1, 10.0)    # Set initial position.
      
      >>> pkt = Packet(0x8e, 0x4f, 0.1)             # Set PPS with to 0.1s
      >>> pkt = Packet(0x8e4f, 0.1)                 # Set PPS with to 0.1s

    """

    code = None
    """The code of the packet. This is always 1 byte, 0x8e or 0x8f with "super-packets"."""

    fields = []
    """The data fields of the packet."""


    def __init__(self, code, *args, **kwargs):

        if code > 255:
            self.code = code >> 8
        else:
            self.code = code

        if self.code in PACKETS_WITH_SUBCODE:
            self.subcode = args[1]
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


    # The packet structure depends `self.code` and `self.subcode`.
    #
    def _get_struct(self):
        try:
            return PACKET_STRUCTURES[self.code][self.subcode]
        except KeyError:
            try:
                return PACKET_STRUCTURES[self.code]
            except KeyError:
                raise ValueError('Invalid packet code/subcode')

    _struct = property(_get_struct)

    def _pack(self):
        """Return binary format of packet.

           The returned string is the binary format of the packet. Neither
           stuffing nor framing has been applied.

        """

        if self.subcode:
            return struct.pack('>BB', self.code, self.subcode) + _struct.pack(self.fields)
        else:
            return struct.pack('>B', self.code) + _struct.pack(self.fields)


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
        if len(packet) >= 2:
            (code, subcode) = struct.unpack('>BB', packet[0:2])
        else:
            (code) = struct.unpack('>B', packet)
            subcode = None


        # Try to find a matching struct.
        #
        try:
            _struct = PACKET_STRUCTURES[code][subcode]
        except KeyError:
            subcode = None
            try:
                _struct = PACKET_STRUCTURES[code]
            except KeyError:
                # Unable to unpack the packet properly. The entire
                # content of `packet` (without the code) will 
                # be the single field of `Packet`.
                _struct = struct.Struct('%ds' % (len(packet)-1))


        # Return an instance of `Packet`.
        print _struct.format, len(packet), '%02x' % code
        if subcode:
            return cls(code, subcode, *_struct.unpack(packet[2:]))
        else:
            return cls(code, *_struct.unpack(packet[1:]))


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


def main():

    with open('thunderbolt.tsip') as reader:
        for packet in GPS(reader):
            print Packet.unpack(packet)



if __name__ == '__main__':
    main()

