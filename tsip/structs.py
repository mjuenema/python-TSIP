# -*- coding: utf-8 -*-
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


# Classes for packing/unpacking TSIP packets whose structure
# cannot be expressed as `struct.Struct()` instances. These 
# mostly deal with packets of variable size/structure/content.
#
class StructNone(object):
    """Structure of packets without payload.
    
       This class represents the strcuture of packets that don't
       have any payload. It provides "dummy" `pack()` and `unpack()`
       methods to maintain the standard interface for managing
       TSIP packet structures. 
    
    """
    
    def pack(self, f=[]):
        return ''
    
    def unpack(self, s=''):
        return []
    
    
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
        return struct.unpack('%ds' % (len(s)), s)
    
    
class Struct0x1c81(object):
    """Report packet 0x1C:81 - Report firmware version.
    
       The product name is of variable length. 
    
    """
    
    fmt = '>BBBBBBH'
    def pack(self, *f):
        return struct.pack(self.fmt, *f[:-1]) + struct.pack('>B', len(f[-1])) + f[-1]
     
    def unpack(self, s):
        print s[9:]
        return struct.unpack(self.fmt, s[:8]) + (s[9:],)
    
    
class Struct0x1c83(object):
    fmt = '>IBBHBH'
    def pack(self, *f):
        return struct.pack(self.fmt, *f[:-1]) + struct.pack('>B', len(f[-1])) + f[-1]
     
    def unpack(self, s):
        return struct.unpack(self.fmt, s[:11]) + (s[12:],)
         
    
    
# class Struct0x47(object):
#     def pack(self, *f):
#         s = struct.pack('>B', len(f)/2)
#         
#         for i in xrange(1, len(f), 2):
#             s += struct.pack('>Bf', f[i], f[i+1])
#             
#         return s 
# 
#     def unpack(self, s):
# 
#         count = struct.unpack('>B', s[0])[0]
#         fields = [count]
# 
#         for i in xrange(0, count):
#             (satnum, siglevel) = struct.unpack('>Bf', s[i+1:i+6])
#             fields.append(satnum)
#             fields.append(siglevel)
# 
#         return fields

class Struct0x58(object):
    def pack(self, *f):
        raise NotImplementedError
    
    def unpack(self, s):
        raise NotImplementedError
    

class Struct0x6d(object):
    """Report Packet 0x6D: Satellite Selection List.
    
       This packet is of variable length equal to 17+nsvs where "nsvs" is 
       the number of satellites used in the solution.
       
    """
    
    
    def pack(self, *f):
        fmt = '>Bffff' + 'b' * (len(f) - 5)
        return struct.pack(fmt, *f)
    
    def unpack(self, s):
        fields = struct.unpack('>Bffff', s[0:17])
        nsvs = (fields[0] & 0b11110000) >> 4
        return fields + struct.unpack('%db' % (nsvs), s[17:])


class Struct0x8ea0(object):
    """Command Packet 0x8E-A0: Set DAC Value.
     
       There are two variants of this packet: Without data, the packet
       is used to request the current DAC voltage. With data, the packet
       is used to set the DAC voltage or value. Furthermore depending
       on the value of byte 1, the DAC value may be set as a value or
       a voltage. 
     
    """
    
    def pack(self, f):
        if f == []:
            return ''
        elif f[0] == 0:
            return struct.pack('>Bf', *f)
        elif f[0] == 1:
            return struct.pack('>BI', *f)
        else:
            raise ValueError
     
    def unpack(self, s=''):
        raise NotImplementedError()
    

# Packet structures.
#
# Keys are the packet codes. Values are lists(!) of instances
# of `struct.Struct()` or class instances providing custom `pack()` 
# and `unpack()` methods for a particular TSIP packet. The values 
# must be lists even if it contains only a single item.
# 
# Packets with sub-codes are two tiered: [code][subcode].
#
PACKET_STRUCTURES = {
    # Command Packet 0x1C - Firmware Version
    0x1c: { 0x01: [StructNone()],
    # Report Packet 0x1C - Firmware Version
            0x81: [Struct0x1c81()],
    # Command Packet 0x1C - Hardware Component Version Information
            0x03: [StructNone()],
    # Report Packet 0x1C - Hardware Component Version Information
            0x83: [Struct0x1c83()], 
          },
    # Command Packet 0x1E - Clear Battery Backup, then Reset
    0x1e: [struct.Struct('>B')],
    # Command Packet 0x1F - Request Software Versions
    0x1f: [StructNone()],
    # Command Packet 0x21 - Request Current Time
    0x21: [StructNone()],
    # Command Packet 0x23 - Initial Position (XYZ ECEF)
    0x23: [struct.Struct('>fff')],
    # Command Packet 0x24: Request GPS Satellite Selection
    0x24: [StructNone()],
    # Command Packet 0x25: Initiate Hot Reset
    0x25: [StructNone()],
    # Command Packet 0x26: Request Receiver Health
    0x26: [StructNone()],
    # Command Packet 0x27: Request Signal Levels
    0x27: [StructNone()],
    # Command Packet 0x29: Request Almanac Health
    0x29: [StructNone()],
    # Command Packet 0x31: Accurate Initial Position (XYZ Cartesian ECEF)
    # Here this packet will always contain double precision values.
    0x31: [struct.Struct('>ddd')],
    # Command Packet 0x32: Accurate Initial Position (LLA)
    # Here this packet will always contain double precision values.
    0x32: [struct.Struct('>ddd')],
    # Command Packet 0x34: Satellite Selection For One-Satellite Mode
    0x34: [struct.Struct('>B')],
    # Command Packet 0x35: Set or Request I/O Options
    0x35: [struct.Struct('>BBBB')],
    # Command Packet 0x37: Request Status and Values of Last Position
    0x37: [StructNone()],
    # Command Packet 0x38: Request Satellite System Data
    0x38: [struct.Struct('>BBB')],
    # Command Packet 0x39: Set or Request SV Disable and Health Use
    0x39: [struct.Struct('>BB')],
    # Command Packet 0x3A: Request Last Raw Measurement
    0x3a: [struct.Struct('>B')],
    # Command Packet 0x3B: Request Ephemeris Status
    0x3b: [struct.Struct('>B')],
    # Command Packet 0x3C: Request Satellite Tracking Status
    0x3c: [struct.Struct('>B')],
    # Command Packet 0x3F-11: Request EEPROM Segment Status
    0x3f: [struct.Struct('>B')],
    # Report Packet 0x42: Single-precision Position Fix
    0x42: [struct.Struct('>ffff')],
    # Report Packet 0x43: Velocity Fix, XYZ ECEF
    0x43: [struct.Struct('>fffff')],
    # Report Packet 0x45: Software Version Information
    0x45: [struct.Struct('>BBBBBBBBBB')],
    # Report Packet 0x46: Receiver Health
    0x46: [struct.Struct('>BB')],
    # Report Packet 0x47: Signals Levels for Tracked Satellites
    # Up to 12 satellite number/signal level pairs may be sent as indicated by 
    # the count field
    0x47: [struct.Struct('BBf'),                   
           struct.Struct('BBfBf'),                   
           struct.Struct('BBfBfBf'),
           struct.Struct('BBfBfBfBf'),             
           struct.Struct('BBfBfBfBfBf'),             
           struct.Struct('BBfBfBfBfBfBf'),    
           struct.Struct('BBfBfBfBfBfBfBf'),       
           struct.Struct('BBfBfBfBfBfBfBfBf'),       
           struct.Struct('BBfBfBfBfBfBfBfBfBf'),
           struct.Struct('BBfBfBfBfBfBfBfBfBfBf'),
           struct.Struct('BBfBfBfBfBfBfBfBfBfBfBf'), 
           struct.Struct('BBfBfBfBfBfBfBfBfBfBfBfBf')],
    # Report Packet 0x49: Almanac Health
    0x49: [struct.Struct('>32B')],
    # Report Packet 0x4A: Single Precision LLA Position Fix
    0x4a: [struct.Struct('>fffff')],
    # Report Packet 0x4B: Receiver Health
    0x4b: [struct.Struct('>BBB')],
    # Report Packet 0x55: I/O Options
    0x55: [struct.Struct('>BBBB')],
    # Report Packet 0x56: Velocity Fix, East-North-Up (ENU)
    0x56: [struct.Struct('>fffff')],
    # Report Packet 0x57: Information about Last Computed Fix
    0x57: [struct.Struct('>BBfI')],
    # Report Packet 0x58: GPS System Data from the Receiver
    0x58: [Struct0x58()], 
    # Report Packet 0x59: Status of Satellite Disable or Ignore Health
    0x59: [struct.Struct('>B32B')],
    # Report Packet 0x5A: Raw Data Measurement Data
    0x5a: [struct.Struct('>Bffffd')],
    # Report Packet 0x5B: Satellite Ephemeris Status
    0x5b: [struct.Struct('>BfBBfBf')],
    # Report Packet 0x5C: Satellite Tracking Status
    0x5c: [struct.Struct('>BBBBffffBBBB')],
    # Report Packet 0x5F-11: EEPROM Segment Status
    0x5f: [StructRaw()],
    # Report Packet 0x6D: Satellite Selection List
    0x6d: [Struct0x6d()],
    # Command/Report Packet 0x70: Filter Configuration
    0x70: [struct.Struct('>BBBB')],
    # Report Packet 0x83: Double Precision XYZ
    0x83: [struct.Struct('>ddddf')],
    # Report Packet 0x84: Double Precision LLA Position (Fix and Bias Information)
    0x84: [struct.Struct('ddddf')],
    # Command/Report Packet 0xBB: Set Receiver Configuration
    0xbb: {0x00: [StructNone(), 
                  struct.Struct('>BBBBBffffBBBBBBBBBBBBBBBBBB')]
           },
    # Command/Report Packet 0xBC: Set Port Configuration
    0xbc: [struct.Struct('>B'), 
           struct.Struct('>BBBBBBBBBB')],
    # TSIP super-packets:
            # Command Packet 0x8E-15: Request current Datum values
    0x8e: { 0x15: [StructNone()],
            # Command Packet 0x8E-26: Write Configuration to NVS
            0x26: [StructNone()],
            # Command Packet 0x8E-41: Request Manufacturing Parameters
            0x41: [StructNone()],
            # Command Packet 0x8E-42: Stored Production Parameters
            0x42: [StructNone()],
            # Command Packet 0x8E-45: Revert Configuration Segment to Default Settings and Write to NVS
            0x45: [struct.Struct('>B')],
            # Command Packet 0x8E-4A: Set PPS Characteristics
            0x4a: [struct.Struct('>BBBdf')],
            # Command Packet 0x8E-4C: Write Configuration Segment to NVS
            0x4c: [struct.Struct('>B')],
            # Command Packet 0x8E-4E: Set PPS output option
            0x4e: [struct.Struct('>B')],
            # Command Packet 0x8E-A0: Set DAC Value
            0xa0: [Struct0x8ea0()],
            # Command Packet 0x8E-A2: UTC/GPS Timing
            0xa2: [struct.Struct('>B')],
            # Command Packet 0x8E-A3: Issue Oscillator Disciplining Command
            0xa3: [struct.Struct('>B')],
            # Command Packet 0x8E-A4: Test Modes
            0xa4: [struct.Struct('>B'), 
                   struct.Struct('>BBHI'), 
                   struct.Struct('>BBffhIHHHh')],
            # Command Packet 0x8E-A5: Packet Broadcast Mask
            0xa5: [struct.Struct('>HH')],
            # Command Packet 0x8E-A6: Self-Survey Command
            0xa6: [struct.Struct('>B')],
            # Command Packet 0x8E-A9: Self-Survey Parameters
            0xa9: [struct.Struct('>BBII'), 
                   StructNone()],
            # Command Packet 0x8E-AB: Request Primary Timing Packet
            0xab: [struct.Struct('>B')],
            # Command Packet 0x8E-AC: Request Supplementary Timing Packet
            0xac: [struct.Struct('>B')]
          },
            # Report Packet 0x8F-15 Current Datum Values
    0x8f: { 0x15: [struct.Struct('>Hddddd')],
            # Report Packet 0x8F-41: Stored Manufacturing Operating Parameters
            0x41: [struct.Struct('>HIBBBBfH')],
            # Report Packet 0x8F-42: Stored Production Parameters
            0x42: [struct.Struct('>BBHIIHHH')],
            # Report Packet 0x8F-4A: Set PPS Characteristics
            0x4a: [struct.Struct('>BBBdf')],
            # Report Packet 0x8F-4E: PPS Output
            0x4e: [struct.Struct('>B')],
            # Report Packet 0x8F-A0: DAC Value
            0xa0: [struct.Struct('>IfBBff')],
            # Report Packet 0x8F-A2: UTC/GPS Timing
            0xa2: [struct.Struct('>B')],
            # Report Packet 0x8F-A3: Oscillator Disciplining Command
            0xa3: [struct.Struct('>B')],
            # Report Packet 0x8F-A5: Packet Broadcast Mask
            0xa5: [struct.Struct('>HH')],
            # Report Packet 0x8F-A6: Self-Survey Command
            0xa6: [struct.Struct('>B')],
            # Report Packet 0x8F-A8: Oscillator Disciplining Parameters
            # TODO
            # Report Packet 0x8F-A9: Self-Survey Parameters
            0xa9: [struct.Struct('>BBII')],
            # Report Packet 0x8F-AB:Primary Timing Packet
            0xab: [struct.Struct('>IHhBBBBBBH')],
            # Report Packet 0x8F-AC: Supplemental Timing Packet
            0xac: [struct.Struct('>BBBIHHBBBBffIffdddfI')]
          }    
}


# List of packets which have a sub-code.
#
PACKETS_WITH_SUBCODE = []
for (key, value) in PACKET_STRUCTURES.items():
    if isinstance(value, types.DictType):
        PACKETS_WITH_SUBCODE.append(key)

def get_structs(code, subcode=None):
    """
    
       :param code: Packet code.
       :type code: Integer.
       :param subcode: Packet subcode or ``None``.
       :type code: Integer or ``None``.
       :return: Possible structures of this packet.
       :rtype: List.
    
    """
    
    if code in PACKETS_WITH_SUBCODE:
        return PACKET_STRUCTURES[code][subcode]
    else:
        return PACKET_STRUCTURES.get(code, [StructRaw()])
        
#         
#     if PACKET_STRUCTURES.has_key(code):
#         if PACKET_STRUCTURES[code].has_key(subcode):
#             return PACKET_STRUCTURES[code][subcode]
#         else:
#             return PACKET_STRUCTURES[code]
#     else:
#         return [StructRaw()]
    
    
    
#     try:
#         return PACKET_STRUCTURES[code].get(subcode)
#     except KeyError:
#         return PACKET_STRUCTURES.get(code)
#     except KeyError:
#         return [StructRaw()]
    
#     if isinstance(value, types.ListType):
#         return value
#     elif isinstance(value, types.DictType):
#         structs_ = value.get(subcode)
#     else:
#         structs_ = [StructRaw()]
#     
#     if not isinstance(structs_, types.ListType):
#         raise ValueError('Invalid packet code/subcode')
#     else:
#         return structs_



def register_packet(code, fmt):
    raise NotImplementedError()
