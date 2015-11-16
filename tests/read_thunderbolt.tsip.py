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
PACKETS_WITH_SUBCODE = [0x8e, 0x8f, 0x1c, 0x7a, 0x7e, 0xbb, 0x5f]


# Classes for packing/unpacking TSIP packets whose structure
# cannot be expressed as `struct.Struct()` instances. These 
# mostly deal with packets of variable size/strcuture/content.
#
class Struct0x47(object):
    def __init__(self):
        pass

    def pack(self, *fields):
        raise NotImplemented()

    def unpack(self, s):

        count = struct.unpack('>B', s[0])
        fields = [count]

        for i in xrange(0, count):
            (satnum, siglevel) = struct.unpack('>Bf', s[i+1:i+5])
            fields.append(satnum)
            fields.append(siglevel)

        return fields

class Struct0x58(object):
    pass

class Struct0x6d(object):
    pass

class Struct0xbb(object):
    pass

class Struct0xbc(object):
    pass


# Packet structures.
#
# Keys are the packet codes. Values can be either an instance
# of `struct.Struct()`, ``None`` if the packet does not contain
# any fields, or a class instance providing custom `pack()` and 
# `unpack()` methods for a particular TSIp packet.
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
    # Command Packet 0x24: Request GPS Satellite Selection
    0x24: None,
    # Command Packet 0x25: Initiate Hot Reset
    0x25: None,
    # Command Packet 0x26: Request Receiver Health
    0x26: None,
    # Command Packet 0x27: Request Signal Levels
    0x27: None,
    # Command Packet 0x29: Request Almanac Health
    0x29: None,
    # Command Packet 0x31: Accurate Initial Position (XYZ Cartesian ECEF)
    # Here this packet will always contain double precision values.
    0x31: struct.Struct('>ddd'),
    # Command Packet 0x32: Accurate Initial Position (LLA)
    # Here this packet will always contain double precision values.
    0x32: struct.Struct('>ddd'),
    # Command Packet 0x34: Satellite Selection For One-Satellite Mode
    0x34: struct.Struct('>B'),
    # Command Packet 0x35: Set or Request I/O Options
    0x35: struct.Struct('>BBBB'),
    # Command Packet 0x37: Request Status and Values of Last Position
    0x37: None,
    # Command Packet 0x38: Request Satellite System Data
    0x38: struct.Struct('>BBB'),
    # Command Packet 0x39: Set or Request SV Disable and Health Use
    0x39: struct.Struct('>BB'),
    # Command Packet 0x3A: Request Last Raw Measurement
    0x3a: struct.Struct('>B'),
    # Command Packet 0x3B: Request Ephemeris Status
    0x3b: struct.Struct('>B'),
    # Command Packet 0x3C: Request Satellite Tracking Status
    0x3c: struct.Struct('>B'),
    # Command Packet 0x3F-11: Request EEPROM Segment Status
    0x3f: strcut.Struct('>B'),
    # Report Packet 0x42: Single-precision Position Fix
    0x42: struct.Struct('>ffff'),
    # Report Packet 0x43: Velocity Fix, XYZ ECEF
    0x43: struct.Struct('>fffff'),
    # Report Packet 0x45: Software Version Information
    0x45: struct.Struct('>BBBBBBBBBB'),
    # Report Packet 0x46: Receiver Health
    0x46: struct.Struct('>BB'),
    # Report Packet 0x47: Signals Levels for Tracked Satellites
    0x47: Struct0x47(),
    # Report Packet 0x49: Almanac Health
    0x49: struct.Struct('>32B'),
    # Report Packet 0x4A: Single Precision LLA Position Fix
    0x4a: struct.Struct('>fffff'),
    # Report Packet 0x4B: Receiver Health
    0x4b: struct.Struct('>BBB'),
    # Report Packet 0x55: I/O Options
    0x55: struct.Struct('>BBBB'),
    # Report Packet 0x56: Velocity Fix, East-North-Up (ENU)
    0x56: struct.Struct('>fffff'),
    # Report Packet 0x57: Information about Last Computed Fix
    0x57: struct.Struct('>BBfI'),
    # Report Packet 0x58: GPS System Data from the Receiver
    0x58: Struct0x58(), 
    # Report Packet 0x59: Status of Satellite Disable or Ignore Health
    0x59: struct.Struct('>B32B'),
    # Report Packet 0x5A: Raw Data Measurement Data
    0x5a: struct.Struct('>Bffffd'),
    # Report Packet 0x5B: Satellite Ephemeris Status
    0x5b: struct.Struct('>BfBBfBf'),
    # Report Packet 0x5C: Satellite Tracking Status
    0x5c: struct.Struct('>BBBBffffBBBB'),
    # Report Packet 0x5F-11: EEPROM Segment Status
    0x5f: { 0x11: struct.Struct('>I') 
          },
    # Report Packet 0x6D: Satellite Selection List
    0x6d: Struct0x6d(),
    # Command/Report Packet 0x70: Filter Configuration
    0x70: struct.Struct('>BBBB'),
    # Report Packet 0x83: Double Precision XYZ
    0x83: struct.Struct('>ddddf'),
    # Report Packet 0x84: Double Precision LLA Position (Fix and Bias Information)
    0x84: struct.Struct('ddddf'),
    # Command/Report Packet 0xBB: Set Receiver Configuration
    0xbb: Struct0xbb(),
    # Command/Report Packet 0xBC: Set Port Configuration
    0xbc: Struct0xbc(),
    # TSIP super-packets:
            # Command Packet 0x8E-15: Request current Datum values
    0x8e: { 0x15: None,
            # Command Packet 0x8E-26: Write Configuration to NVS
            0x26: None,
            # Command Packet 0x8E-41: Request Manufacturing Parameters
            0x41: none
          }
    
}


# Contants for setting bits
#
BIT0 = B0 = 0b00000001
BIT1 = B1 = 0b00000010
BIT2 = B2 = 0b00000100
BIT3 = B3 = 0b00001000
BIT4 = B4 = 0b00010000
BIT5 = B5 = 0b00100000
BIT6 = B6 = 0b01000000
BIT7 = B7 = 0b10000000


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

    def pack(self):
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

