
from struct import Struct
from binascii import hexlify

from tsip import *

class Test0x1c(object):

    def test_0x1c01(self):
        """Command packet 0x1C:01 - Firmware version"""
        pkt = Packet(0x1c, 0x01)
        assert pkt.code == 0x1c
        assert pkt.subcode == 0x01
        assert pkt.fields == []
        
        assert isinstance(pkt._struct, StructNone)
        assert hexlify(pkt.pack()) == '1c01'
        
    def test_0x1c81(self):
        """Report packet 0x1C:81 - Report firmware version"""
        pkt = Packet(0x1c, 0x81, 0, 3, 2, 1, 11, 17, 2015, 'productname')
        assert pkt.code == 0x1c
        assert pkt.subcode == 0x81
        assert pkt.fields[0] == 0
        assert pkt.fields[1] == 3
        assert pkt.fields[2] == 2
        assert pkt.fields[3] == 1
        assert pkt.fields[4] == 11
        assert pkt.fields[5] == 17
        assert pkt.fields[6] == 2015
        assert pkt.fields[7] == 'productname'
        
        assert isinstance(pkt._struct, Struct0x1c81)
        assert hexlify(pkt.pack()) == '1c81000302010b1107df0b70726f647563746e616d65'
         
        
    def test_0x1c03(self):
        """Command packet 0x1C:03 - Hardware component version information"""
        pkt = Packet(0x1c, 0x03)
        assert pkt.code == 0x1c
        assert pkt.subcode == 0x03
        assert pkt.fields == []
        
        assert isinstance(pkt._struct, StructNone)
        assert hexlify(pkt.pack()) == '1c03'
            
