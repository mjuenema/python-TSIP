#-*- coding: utf-8 -*-
"""
Binary structures of TSIP packets.

The mechanisms for "packing" and "unpacking" TSIP packets
do not check at all whether values are valid or even sensible.

The rationale behind this descision is to avoid conflict with
any future changes to the TSIP protocol by the vendor. It is
entirely up to the user to ensure that the TSIP packets they
create are valid.

"""

import struct
import types

from tsip.config import *


MAX_PRODUCTNAME_LEN = 30
"""Maximum lenght of the GPS's product name."""

MAX_CHANNELS = 12
"""Maximum number of channels a GPS model supports."""


# Classes for packing/unpacking TSIP packets whose structure
# cannot be expressed as `struct.Struct()` instances. These
# mostly deal with packets of variable size/structure/content.
#
# class StructNone(object):
#     """Structure of packets without payload.
#
#        This class represents the strcuture of packets that don't
#        have any payload. It provides "dummy" `pack()` and `unpack()`
#        methods to maintain the standard interface for managing
#        TSIP packet structures.
#
#     """
#
#     def pack(self, *f):
#         return ''
#
#     def unpack(self, s=''):
#         return []
#

def tobytes(s):
    try:
        return bytes(s.encode())
    except AttributeError:
        return s
    except UnicodeDecodeError:
        return bytes(s)             # a no-op in Python 2


def unpack(fmt, x):

    # In Python 3 extracting a single index out of a bytes "string"
    # returns an integer whereas Python 2 returned a single-character
    # string (see tsip/structs.py", line 498, in get_structs_for_rawpacket).
    if isinstance(x, int):
        return [x]
    else:
        return list(struct.unpack(fmt, tobytes(x)))


class Struct(struct.Struct):
    """Custom `struct.Struct` class.

       This class implements the following changes to the original
       `struct.Struct` class.

       * the return value of `unpack()` is a list instead of a tuple.

         >>> s = Struct('BB')
         >>> s.unpack('\x01\x02')
         [1, 2]	# not (1, 2,)

       * some issues regarding Python 2 strings versus Python 3 unicode strings
         and byte-arrays are dealt with transparently.

       * add `unpack_slice()` method which transparently deals
         with Python 2 and Python 3 differences (strings vs. bytes).

    """

    def __init__(self, *args, **kwargs):
        super(Struct, self).__init__(*args, **kwargs)

    def unpack(self, x):
#        try:
#            x = bytes(x.encode())          # Python 3
#        except UnicodeDecodeError:
#            pass                           # Python 2

        return list(super(Struct, self).unpack(tobytes(x)))

#    def unpack_slice(x, i, j):
#        try:
#            y = x[i:j]         # Python 2
#        except TypeError:
#            y = bytes(x)[i:j]  # Python 2
#
#        return list(super(Struct, self).unpack(y))



class StructRaw(object):
    """Structure of packets that are interpreted as raw data.

       The `StructRaw` class is used for packets for which the
       structure is not implemented anywhere else. Such packets
       are interpreted as containing a single field holding
       the entire packet payload.

    """

    def pack(self, *f):
        raise NotImplementedError()

    def unpack(self, s):
        return struct.unpack('>%ds' % (len(s)), s)


class Struct0x1c81(object):
    """Report packet 0x1C:81 - Report firmware version.

       The product name is of variable length.

    """

    format = '>BBBBBBBBH'

    def pack(self, *f):
        return struct.pack(self.format, *f[:-1]) + struct.pack('>B', len(f[-1])) + tobytes(f[-1])

    def unpack(self, rawpacket):
        return struct.unpack(self.format, rawpacket[:10]) + (rawpacket[11:].decode(),)


class Struct0x1c83(object):
    format = '>BBIBBHBH'

    def pack(self, *f):
        return struct.pack(self.format, *f[:-1]) + struct.pack('>B', len(f[-1])) + tobytes(f[-1])

    def unpack(self, s):
        return struct.unpack(self.format, s[:13]) + (s[14:].decode(),)

class Struct0x47(object):
    def pack(self, *f):
        raise NotImplemented

    def unpack(self, s):
        count = struct.unpack('>B', s[1])[0]
        fields = [0x47, count]

        for i in range(0, count-1):
            i1 = 2 + i * 5
            i2 = 2 + i * 5 + 5
            (satnum, siglevel) = struct.unpack('>Bf', s[i1:i2])
            fields.append(satnum)
            fields.append(siglevel)

        return fields


class Struct0x58(object):
    # ONLY TESTED WITH COPERNICUS II

    def pack(self, *f):
        raise NotImplementedError

    def unpack(self, s):
        fields = list(struct.unpack('>BBBBB', s[:5]))

        type_of_data = fields[2]
        s = s[5:]

        if type_of_data == 2:
            # Almanac
            fields += list(struct.unpack('>BBfffffffffffffffHH', s))
        elif type_of_data == 3:
            # Health page
            fields += list(struct.unpack('>BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBh', s))
        elif type_of_data == 4:
            # Ionospheric
            fields += list(struct.unpack('>ffffffff', s[8:]))
        elif type_of_data == 5:
            # UTC
            fields += list(struct.unpack('>dfhfHHHh', s[13:]))
        elif type_of_data == 6:
            # Ephemeris
            fields += list(struct.unpack('>BfhBBBBhffffffBBffdfdfdffdfdfdffddddd', s))

        return fields
        

class Struct0x6d(object):
    """Report Packet 0x6D: Satellite Selection List.

       This packet is of variable length equal to 5+nsvs where "nsvs" is
       the number of satellites used in the solution.

    """


    def pack(self, *f):
        fmt = '>Bffff' + 'b' * (len(f) - 5)
        return struct.pack(fmt, *f)

    def unpack(self, s):
        fields = [0x6d] + list(struct.unpack('>Bffff', s[1:18]))
        nsvs = (fields[0] & 0b11110000) >> 4

        try:
            s = s[18:]
            for n in range(0, nsvs):
                fields.append(struct.unpack('>b', s[n])[0])
        except IndexError:
            # Occasionally `s` doesn't seem to be long enough
            # so in this case instead of causing an exception we
            # simply return the data so far.
            pass

        return fields


class Struct0xbb(object):
    """Set/get receiver configuration.

       Packet 0xbb/subcode=0 may be used to either query the current receiver
       configuration or change it. The packet contains fields that must contain
       ``0xff``.

    """
    format = '>BBBBBBffffBBBBBBBBBBBBBBBBBBB'

    def pack(self, *fields):

        #
        #
        if not fields:
            # 0xbb query mode is handled by StructNone(); raise struct.error
            # so the calling function can detect this.
            #
            raise struct.error
        else:
            # Ensure that fields 1, 3, 8 (index starts a zero!) and the trailing
            # bytes contain 0xff.
            #
            fields = list(fields)         # Convert to list as tuples are immutable.
            fields[3] = fields[5] = fields[10] = 0xff
            fields = fields[0:12] + [0xff] * 17
            return struct.pack(self.format, *fields)

    def unpack(self, rawpacket):
        return struct.unpack(self.format, rawpacket)



class Struct0x8ea0(object):
    """Command Packet 0x8E-A0: Set DAC Value.

       There are three variants of this packet: Without data, the packet
       is used to request the current DAC voltage. With data, the packet
       is used to set the DAC voltage or value. Furthermore depending
       on the value of byte 1, the DAC value may be set as a value or
       a voltage.

    """

    def pack(self, *fields):
        if fields == (0x8e, 0xa0):
            return struct.pack('>BB', *fields)
        elif fields[2] == 0:
            return struct.pack('>BBBf', *fields)
        elif fields[2] == 1:
            return struct.pack('>BBBI', *fields)
        else:
            raise ValueError

    def unpack(self, rawpacket):

        try:
            flag = unpack('>B', rawpacket[2])[0]
        except IndexError:
            return unpack('>BB', rawpacket)

        if flag == 0:
            return unpack('>BBBf', rawpacket)
        elif flag == 1:
            return unpack('>BBBI', rawpacket)
        else:
            raise ValueError('Invalid flag in packet 0x8ea0')


class Struct0x8ea8(object):
    fmt0 = '>BBBff'
    fmt1 = '>BBBfff'
    fmt2 = '>BBBff'
    fmt3 = '>BBBf'

    def pack(self, *fields):
        type_ = fields[2]

        if type_ == 0:
            return struct.pack(self.fmt0, *fields)
        elif type_ == 1:
            return struct.pack(self.fmt1, *fields)
        elif type_ == 2:
            return struct.pack(self.fmt2, *fields)
        elif type_ == 3:
            return struct.pack(self.fmt3, *fields)
        else:
            raise ValueError('Invalid type in packet 0x8ea8')

    def unpack(self, rawpacket):
        type_ = unpack('>B', rawpacket[2])[0]

        if type_ == 0:
            return unpack(self.fmt0, rawpacket)
        elif type_ == 1:
            return unpack(self.fmt1, rawpacket)
        elif type_ == 2:
            return unpack(self.fmt2, rawpacket)
        elif type_ == 3:
            return unpack(self.fmt3, rawpacket)
        else:
            raise ValueError('Invalid type in packet 0x8ea8')


Struct0x8fa8 = Struct0x8ea8


# Packet structures.
#
# Keys are the packet codes/subcodes. Values are lists(!) of instances
# of `Struct()` or class instances providing custom `pack()`
# and `unpack()` methods for a particular TSIP packet. The values
# must be lists even if it contains only a single item.
#
PACKET_STRUCTURES = {
    # Report packet 0X13 unparsable packet
    # TODO: Report packet 0X13 unparsable packe
    # Command Packet 0x1C - Firmware Version
    0x1c01: [Struct('>BB')],
    # Report Packet 0x1C - Firmware Version
    0x1c81: [Struct0x1c81()],
    # Command Packet 0x1C - Hardware Component Version Information
    0x1c03: [Struct('>BB')],
    # Report Packet 0x1C - Hardware Component Version Information
    0x1c83: [Struct0x1c83()],
    # Command Packet 0x1E - Clear Battery Backup, then Reset
    0x1e:   [Struct('>BB')],
    # Command Packet 0x1F - Request Software Versions
    0x1f:   [Struct('>B')],
    # Command Packet 0x21 - Request Current Time
    0x21:   [Struct('>B')],
    # Command Packet 0x23 - Initial Position (XYZ ECEF)
    0x23:   [Struct('>Bfff')],
    # Command Packet 0x24: Request GPS Satellite Selection
    0x24:   [Struct('>B')],
    # Command Packet 0x25: Initiate Hot Reset
    0x25:   [Struct('>B')],
    # Command Packet 0x26: Request Receiver Health
    0x26:   [Struct('>B')],
    # Command Packet 0x27: Request Signal Levels
    0x27:   [Struct('>B')],
    # Command Packet 0x29: Request Almanac Health
    0x29:   [Struct('>B')],
    # Command Packet 0x2d: request oscillator offset
    0x2d:   [Struct('>B')],
    # Command Packet 0x31: Accurate Initial Position (XYZ Cartesian ECEF)
    # Here this packet will always contain double precision values.
    0x31:   [Struct('>Bddd')],
    # Command Packet 0x32: Accurate Initial Position (LLA)
    # Here this packet will always contain double precision values.
    0x32:   [Struct('>Bddd')],
    # Command Packet 0x34: Satellite Selection For One-Satellite Mode
    0x34:   [Struct('>BB')],
    # Command Packet 0x35: Set or Request I/O Options
    0x35:   [Struct('>BBBBB')],
    # Command Packet 0x37: Request Status and Values of Last Position
    0x37:   [Struct('>B')],
    # Command Packet 0x38: Request Satellite System Data
    0x38:   [Struct('>BBBB')],
    # Command Packet 0x39: Set or Request SV Disable and Health Use
    0x39:   [Struct('>BBB')],
    # Command Packet 0x3A: Request Last Raw Measurement
    0x3a:   [Struct('>BB')],
    # Command Packet 0x3B: Request Ephemeris Status
    0x3b:   [Struct('>BB')],
    # Command Packet 0x3C: Request Satellite Tracking Status
    0x3c:   [Struct('>BB')],
    # Command Packet 0x3F-11: Request EEPROM Segment Status
    0x3f:   [Struct('>BB')],
    # Report packet 0x41: GPS Time
    0x41:   [Struct('>Bfhf')],
    # Report Packet 0x42: Single-precision Position Fix
    0x42:   [Struct('>Bffff')],
    # Report Packet 0x43: Velocity Fix, XYZ ECEF
    0x43:   [Struct('>Bfffff')],
    # Report Packet 0x45: Software Version Information
    0x45:   [Struct('>BBBBBBBBBBB')],
    # Report Packet 0x46: Receiver Health
    # In contradiction to the official documentation packet 0x46 may occur
    # with only single unsigned integer field.
    0x46:   [Struct('>BBB'), Struct('>B')],
    # Report Packet 0x47: Signals Levels for Tracked Satellites
    # Up to 12 satellite number/signal level pairs may be sent as indicated by
    # the count field
    0x47:   [Struct0x47()],
    # Report Packet 0x49: Almanac Health
    0x49:   [Struct('>B32B')],
    # Report Packet 0x4A: Single Precision LLA Position Fix
    0x4a:   [Struct('>Bfffff')],
    # Report Packet 0x4B: Receiver Health
    0x4b:   [Struct('>BBBB')],
    # Report Packet 0x4d: Oscillator offset
    0x4d:   [Struct('>Bf')],
    # Report Packet 0x55: I/O Options
    0x55:   [Struct('>BBBBB')],
    # Report Packet 0x56: Velocity Fix, East-North-Up (ENU)
    0x56:   [Struct('>Bfffff')],
    # Report Packet 0x57: Information about Last Computed Fix
    0x57:   [Struct('>BBBfI')],
    # Report Packet 0x58: GPS System Data from the Receiver
    0x58:   [Struct0x58()],
    # Report Packet 0x59: Status of Satellite Disable or Ignore Health
    0x59:   [Struct('>BB32B')],
    # Report Packet 0x5A: Raw Data Measurement Data
    0x5a:   [Struct('>BBffffd')],
    # Report Packet 0x5B: Satellite Ephemeris Status
    0x5b:   [Struct('>BfBBfBf')],
    # Report Packet 0x5C: Satellite Tracking Status
    0x5c:   [Struct('>BBBBBffffBBBB')],
    # Report Packet 0x5F-11: EEPROM Segment Status
    0x5f:   [StructRaw()],
    # Report Packet 0x6D: Satellite Selection List
    0x6d:   [Struct0x6d()],
    # Command/Report Packet 0x70: Filter Configuration
    0x70:   [Struct('>BBBBB')],
    # Report Packet 0x82: SBAS correction status
    0x82:   [Struct('>BB')],
    # Report Packet 0x83: Double Precision XYZ
    0x83:   [Struct('>Bddddf')],
    # Report Packet 0x84: Double Precision LLA Position (Fix and Bias Information)
    0x84:   [Struct('>Bddddf')],
    # Command/Report Packet 0xBB: Set Receiver Configuration
    0xbb00: [Struct('>BB'), Struct0xbb()],
    # Command/Report Packet 0xBC: Set Port Configuration
    0xbc:   [Struct('>BB'), Struct('>BBBBBBBBBBB')],
    # Command Packet 0x8E-15: Request current Datum values
    0x8e15: [Struct('>BB')],
    # Command Packet 0x8E-23 - Request Last Compact Fix Information
    0x8e23: [Struct('>BBB')],
    # Command Packet 0x8E-26: Write Configuration to NVS
    0x8e26: [Struct('>BB')],
    # Command Packet 0x8E-41: Request Manufacturing Parameters
    0x8e41: [Struct('>BB')],
    # Command Packet 0x8E-42: Stored Production Parameters
    0x8e42: [Struct('>BB')],
    # Command Packet 0x8E-45: Revert Configuration Segment to Default Settings and Write to NVS
    0x8e45: [Struct('>BBB')],
    # Command Packet 0x8E-4A: Set PPS Characteristics
    0x8e4a: [Struct('>BBBBBdf')],
    # Command Packet 0x8E-4C: Write Configuration Segment to NVS
    0x8e4c: [Struct('>BBB')],
    # Command Packet 0x8E-4E: Set PPS output option
    0x8e4e: [Struct('>BBB')],
    # Command Packet 0x8E-A0: Set DAC Value
    0x8ea0: [Struct0x8ea0()],
    # Command Packet 0x8E-A2: UTC/GPS Timing
    0x8ea2: [Struct('>BBB')],
    # Command Packet 0x8E-A3: Issue Oscillator Disciplining Command
    0x8ea3: [Struct('>BBB')],
    # Command Packet 0x8E-A4: Test Modes
    0x8ea4: [Struct('>BBB'), Struct('>BBBHI'), Struct('>BBBffhIHHHh')],
    # Command Packet 0x8E-A5: Packet Broadcast Mask
    0x8ea5: [Struct('>BBHH')],
    # Command Packet 0x8E-A6: Self-Survey Command
    0x8ea6: [Struct('>BBB')],
    # Command Packet 0x8E-A8: Set or Request Disciplining Parameters
    0x8ea8: [Struct0x8ea8()],
    # Command Packet 0x8E-A9: Self-Survey Parameters
    0x8ea9: [Struct('>BBBBII'), Struct('>BBB')],
    # Command Packet 0x8E-AB: Request Primary Timing Packet
    0x8eab: [Struct('>BBB')],
    # Command Packet 0x8E-AC: Request Supplementary Timing Packet
    0x8eac: [Struct('>BBB')],
    # Report Packet 0x8F-15 Current Datum Values
    0x8f15: [Struct('>BBhddddd')],
    # Report Packet 0x8F-23 - Request Last Compact Fix Information
    0x8f23: [Struct('>BBIHBBiIihhhh')],
    # Report Packet 0x8F-41: Stored Manufacturing Operating Parameters
    0x8f41: [Struct('>BBHIBBBBfH')],
    # Report Packet 0x8F-42: Stored Production Parameters
    0x8f42: [Struct('>BBBBHIIHHH')],
    # Report Packet 0x8F-4A: Set PPS Characteristics
    0x8f4a: [Struct('>BBBBBdf')],
    # Report Packet 0x8F-4E: PPS Output
    0x8f4e: [Struct('>BBB')],
    # Report Packet 0x8F-A0: DAC Value
    0x8fa0: [Struct('>BBIfBBff')],
    # Report Packet 0x8F-A2: UTC/GPS Timing
    0x8fa2: [Struct('>BBB')],
    # Report Packet 0x8F-A3: Oscillator Disciplining Command
    0x8fa3: [Struct('>BBB')],
    # Report Packet 0x8F-A4: Test Modes
    0x8fa4: [Struct('>BBB'), Struct('>BBBHI'), Struct('>BBBffhIHHHh')],
    # Report Packet 0x8F-A5: Packet Broadcast Mask
    0x8fa5: [Struct('>BBHH')],
    # Report Packet 0x8F-A6: Self-Survey Command
    0x8fa6: [Struct('>BBB')],
    # Report Packet 0x8F-A8: Oscillator Disciplining Parameters
    0x8fa8: [Struct0x8fa8()],
    # Report Packet 0x8F-A9: Self-Survey Parameters
    0x8fa9: [Struct('>BBBBII')],
    # Report Packet 0x8F-AB:Primary Timing Packet
    0x8fab: [Struct('>BBIHhBBBBBBH')],
    # Report Packet 0x8F-AC: Supplemental Timing Packet
    0x8fac: [Struct('>BBBBBIHHBBBBffIffdddfI')]
}


def get_structs_for_rawpacket(rawpacket):
    """

       :param rawpacket: Packet code.
       :type rawpacket: Binary string.
       :return: Possible structures of this packet. May be an empty list.
       :rtype: List.

    """

    key = unpack('>B', rawpacket[0])[0]

    try:
        return PACKET_STRUCTURES[key]
    except KeyError:
        try:
            key = unpack('>H', rawpacket[0:2])[0]
            return PACKET_STRUCTURES[key]
        except (struct.error, KeyError):
            return []


def get_structs_for_fields(fields):

    key = fields[0]

    try:
        return PACKET_STRUCTURES[key]
    except KeyError:
        try:
            key = fields[0] * 256 + fields[1]
            return PACKET_STRUCTURES[key]
        except (IndexError, KeyError):
            return []



def register_packet(code, fmt):
    raise NotImplementedError()
