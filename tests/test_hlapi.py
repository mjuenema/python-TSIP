
from struct import Struct

from tsip import *

class PacketTest(object):
    (code, subcode, fields, binary) = (None, None, [], '')
    
    def setup(self):
        if self.subcode is not None:
            self.pkt1 = Packet(self.code, self.subcode, *self.fields)
        else:
            self.pkt1 = Packet(self.code, *self.fields)

    def test(self):
        assert self.pkt1.code == self.code
        if self.subcode is not None:
            assert self.pkt1.subcode == self.subcode      
        assert self.pkt1.fields == self.fields
        assert self.pkt1.pack() == self.binary
    
        pkt2 = Packet.unpack(self.binary)
        assert pkt2.code == self.code
        if self.subcode is not None:
            assert pkt2.subcode == self.subcode      # may be None
        assert pkt2.fields == self.fields
        assert pkt2.pack() == self.binary
    
    
class Test0x1c01(PacketTest):
    (code, subcode, fields, binary) = (0x1c, 0x01, [], '\x1c\x01')
    
class Test0x1c81(PacketTest):
    (code, subcode, fields, binary) = (0x1c, 0x81, [0, 3, 2, 1, 11, 17, 2015, 'productname'], 
                                       '\x1c\x81\x00\x03\x02\x01\x0b\x11\x07\xdf\x0bproductname')
class Test0x1c03(PacketTest):    
    (code, subcode, fields, binary) = (0x1c, 0x03, [], '\x1c\x03')
    
class Test0x1c83(PacketTest):
    (code, subcode, fields, binary) = (0x1c, 0x83, [1234567890, 17, 11, 2015, 15, 987, 'hardwareid'],
                                       '\x1c\x83I\x96\x02\xd2\x11\x0b\x07\xdf\x0f\x03\xdb\nhardwareid')
class Test0x1e(PacketTest):
    (code, subcode, fields, binary) = (0x1e, None, [0x4b], '\x1e\x4b')
    
class Test0x1f(PacketTest):
    (code, subcode, fields, binary) = (0x1f, None, [], '\x1f')
    
class Test0x24(PacketTest):
    (code, subcode, fields, binary) = (0x24, None, [], '\x24')
    
class Test0x25(PacketTest):
    (code, subcode, fields, binary) = (0x25, None, [], '\x25')
    
class Test0x26(PacketTest):
    (code, subcode, fields, binary) = (0x26, None, [], '\x26')
    
class Test0x27(PacketTest):
    (code, subcode, fields, binary) = (0x27, None, [], '\x27')
    
class Test0x29(PacketTest):
    (code, subcode, fields, binary) = (0x29, None, [], '\x29')
    
class Test0x31(PacketTest):
    (code, subcode, fields, binary) = (0x31, None, [10.0, 20.0, 30.0], 
                                       '1@$\x00\x00\x00\x00\x00\x00@4\x00\x00\x00\x00\x00\x00@>\x00\x00\x00\x00\x00\x00')
    
class Test0x32(PacketTest):
    (code, subcode, fields, binary) = (0x32, None, [-10.0, -20.0, 30.0],
                                       '2\xc0$\x00\x00\x00\x00\x00\x00\xc04\x00\x00\x00\x00\x00\x00@>\x00\x00\x00\x00\x00\x00')
    
class Test0x34(PacketTest):
    (code, subcode, fields, binary) = (0x34, None, [0x32], '\x34\x32') 
    
class Test0x35(PacketTest):
    (code, subcode, fields, binary) = (0x35, None, [0, 1, 2, 3], '\x35\x00\x01\x02\x03')
        
class Test0x37(PacketTest):
    (code, subcode, fields, binary) = (0x37, None, [], '\x37')
    
class Test0x38(PacketTest):
    (code, subcode, fields, binary) = (0x38, None, [1, 2, 3], '\x38\x01\x02\x03')
    
class Test0x39(PacketTest):
    (code, subcode, fields, binary) = (0x39, None, [1, 2], '\x39\x01\x02')
    
class Test0x3a(PacketTest):
    (code, subcode, fields, binary) = (0x3a, None, [1], '\x3a\x01')
    
class Test0x3b(PacketTest):
    (code, subcode, fields, binary) = (0x3b, None, [1], '\x3b\x01')
    
class Test0x3c(PacketTest):
    (code, subcode, fields, binary) = (0x3c, None, [1], '\x3c\x01')
    
class Test0x3f(PacketTest):
    (code, subcode, fields, binary) = (0x3f, None, [1], '\x3f\x01')
    
class Test0x42(PacketTest):
    (code, subcode, fields, binary) = (0x42, None, [-10.0, 20.0, 30.0, 40.0], 
                                       'B\xc1 \x00\x00A\xa0\x00\x00A\xf0\x00\x00B \x00\x00')
        
class Test0x43(PacketTest):
    (code, subcode, fields, binary) = (0x43, None, [-10.0, 20.0, 30.0, 40.0, 50.0], 
                                       'C\xc1 \x00\x00A\xa0\x00\x00A\xf0\x00\x00B \x00\x00BH\x00\x00')
    
class Test0x45(PacketTest):
    (code, subcode, fields, binary) = (0x45, None, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                                       'E\x00\x01\x02\x03\x04\x05\x06\x07\x08\t')
    
class Test0x46(PacketTest):
    (code, subcode, fields, binary) = (0x46, None, [0, 1], 'F\x00\x01')

class Test0x47_1(PacketTest):
    (code, subcode, fields, binary) = (0x47, None, [1, 2, 20.0], 'G\x01\x02\x00\x00\x00\x00\xa0A')
    
class Test0x47_2(PacketTest):
    (code, subcode, fields, binary) = (0x47, None, [3, 2, 20.0, 3, 30.0, 4, 40.0],
                                       'G\x03\x02\x00\x00\x00\x00\xa0A\x03\x00\x00\x00\x00\x00\xf0A\x04\x00\x00\x00\x00\x00 B')
    
class Test0x49(PacketTest):
    (code, subcode, fields, binary) = (0x49, None, [0] * 32, 
                                       'I\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    
class Test0x4a(PacketTest):
    (code, subcode, fields, binary) = (0x4a, None, [10.0, 20.0, 30.0, 40.0, 50.0],
                                                    'JA \x00\x00A\xa0\x00\x00A\xf0\x00\x00B \x00\x00BH\x00\x00')

class Test0x4b(PacketTest):
    (code, subcode, fields, binary) = (0x4b, None, [96, 1, 2], 'K`\x01\x02')
    
class Test0x55(PacketTest):
    (code, subcode, fields, binary) = (0x55, None, [0, 1, 2, 3], 'U\x00\x01\x02\x03')

class Test0x57(PacketTest):
    (code, subcode, fields, binary) = (0x57, None, [0, 1, 10.0, 1000], 'W\x00\x01A \x00\x00\x00\x00\x03\xe8')      
    
#  TODO: class Test0x58(PacketTest):

class Test0x5a(PacketTest):
    (code, subcode, fields, binary) = (0x5a, None, [0, 10.0, 20.0, 30.0, 40.0, 50.0], 
                                                    'Z\x00A \x00\x00A\xa0\x00\x00A\xf0\x00\x00B \x00\x00@I\x00\x00\x00\x00\x00\x00')
    
class Test0x5c(PacketTest):
    (code, subcode, fields, binary) = (0x5c, None, [0, 1, 3, 4, 10.0, 20.0, 30.0, 40.0, 5, 6, 7, 8],
                                                    '\\\x00\x01\x03\x04A \x00\x00A\xa0\x00\x00A\xf0\x00\x00B \x00\x00\x05\x06\x07\x08')

# class Test0x5f(PacketTest):
#     (code, subcode, fields, binary) = (0x5f, 0x11, [1000], '_\x11\x00\x00\x03\xe8')
    
# class Test0x6d(PacketTest):
#     (code, subcode, fields, binary) = (0x6d, None, [3, 10.0, 20.0, 30.0, 40.0, -1, -2, -3], 
#                                        'm\x03A \x00\x00A\xa0\x00\x00A\xf0\x00\x00B \x00\x00\xff\xfe\xfd')

class Test0x70(PacketTest):
    (code, subcode, fields, binary) = (0x70, None, [0, 1, 0, 1], 'p\x00\x01\x00\x01')

class Test0x83(PacketTest):
    (code, subcode, fields, binary) = (0x83, None, [10.0, 20.0, 30.0, 40.0, 50.0],
                                       '\x83@$\x00\x00\x00\x00\x00\x00@4\x00\x00\x00\x00\x00\x00@>\x00\x00\x00\x00\x00\x00@D\x00\x00\x00\x00\x00\x00BH\x00\x00')
    
class Test0x84(PacketTest):
    (code, subcode, fields, binary) = (0x84, None, [10.0, 20.0, 30.0, 40.0, 50.0],
                                       '\x84\x00\x00\x00\x00\x00\x00$@\x00\x00\x00\x00\x00\x004@\x00\x00\x00\x00\x00\x00>@\x00\x00\x00\x00\x00\x00D@\x00\x00HB')
    
class Test0xbb_1(PacketTest):
    (code, subcode, fields, binary) = (0xbb, 0x00, [], '\xbb\x00')
