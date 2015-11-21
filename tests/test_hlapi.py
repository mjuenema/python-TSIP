
from struct import Struct

from tsip import *

class PacketTest(object):
    (code, subcode, fields, binary) = (None, None, [], '')
    
    def setup(self):
        if self.subcode is not None:
            self.pkt1 = Packet(self.code, self.subcode, *self.fields)
        else:
            self.pkt1 = Packet(self.code, *self.fields)
            
        self.pkt2 = Packet.unpack(self.binary)

    def test_pack(self):
        assert self.pkt1.code == self.code
        if self.subcode is not None:
            assert self.pkt1.subcode == self.subcode      
        assert self.pkt1.fields == self.fields
        assert self.pkt1.pack() == self.binary
    
    def test_unpack(self):
        assert self.pkt2.code == self.code
        if self.subcode is not None:
            assert self.pkt2.subcode == self.subcode      # may be None
        assert self.pkt2.fields == self.fields
        assert self.pkt2.pack() == self.binary
        
    def test_fields(self):
        for i in xrange(0, len(self.pkt1.fields)):
            assert self.pkt1.fields[i] == self.pkt1[i]
            self.pkt1[i] = i
            assert self.pkt1[i] == self.pkt1.fields[i] == i 
            
        for i in xrange(0, len(self.pkt2.fields)):
            assert self.pkt2.fields[i] == self.pkt2[i]
            self.pkt2[i] = i
            assert self.pkt2[i] == self.pkt2.fields[i] == i
            
    def test_repr(self):
        assert str(self.pkt1) == str(self.pkt2) 
            

    
    
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
    
class Test0x2d(PacketTest):
    (code, subcode, fields, binary) = (0x2d, None, [], '\x2d')
    
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

class Test0x41(PacketTest):
    (code, subcode, fields, binary) = (0x41, None, [-10.0, -20, 30.0], 
                                       'A\xc1 \x00\x00\xff\xecA\xf0\x00\x00')
    
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
    (code, subcode, fields, binary) = (0x47, None, [1, 2, 20.0], 'G\x01\x02A\xa0\x00\x00')
    
class Test0x47_2(PacketTest):
    (code, subcode, fields, binary) = (0x47, None, [3, 2, 20.0, 3, 30.0, 4, 40.0],
                                       'G\x03\x02A\xa0\x00\x00\x03A\xf0\x00\x00\x04B \x00\x00')
    
class Test0x49(PacketTest):
    (code, subcode, fields, binary) = (0x49, None, [0] * 32, 
                                       'I\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    
class Test0x4a(PacketTest):
    (code, subcode, fields, binary) = (0x4a, None, [10.0, 20.0, 30.0, 40.0, 50.0],
                                                    'JA \x00\x00A\xa0\x00\x00A\xf0\x00\x00B \x00\x00BH\x00\x00')

class Test0x4b(PacketTest):
    (code, subcode, fields, binary) = (0x4b, None, [96, 1, 2], 'K`\x01\x02')
    
class Test0x4d(PacketTest):
    (code, subcode, fields, binary) = (0x4d, None, [10.0], 'MA \x00\x00')
    
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
    
class PacketTest0xbb(PacketTest):
    fields1 = []
    fields2 = []
    def test_pack(self):
        assert self.pkt1.code == self.code
        assert self.pkt1.subcode == self.subcode      
        assert self.pkt1.fields == self.fields1
        assert self.pkt1.pack() == self.binary
      
    def test_unpack(self):
        assert self.pkt2.code == self.code
        assert self.pkt2.subcode == self.subcode
        assert self.pkt2.fields == self.fields2
        assert self.pkt2.pack() == self.binary
        
    def test_repr(self):
        # self.pkt2 has the trailing 0xff added!
        pass 
    
class Test0xbb_2(PacketTest0xbb):
    (code, subcode, fields, binary) = (0xbb, 0x00, [0, 0xff, 1, 0xff, -1.0, -1.0, -1.0, -1.0, 0xff, 2], 
                                       '\xbb\x00\x00\xff\x01\xff\xbf\x80\x00\x00\xbf\x80\x00\x00\xbf\x80\x00\x00\xbf\x80\x00\x00\xff\x02\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')
    fields1 = [0, 255, 1, 255, -1.0, -1.0, -1.0, -1.0, 255, 2]
    fields2 = [0, 255, 1, 255, -1.0, -1.0, -1.0, -1.0, 255, 2, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]

class Test0xbb_3(PacketTest0xbb):
    (code, subcode, fields, binary) = (0xbb, 0x00, [0, 9, 1, 9, -1.0, -1.0, -1.0, -1.0, 9, 2], 
                                       '\xbb\x00\x00\xff\x01\xff\xbf\x80\x00\x00\xbf\x80\x00\x00\xbf\x80\x00\x00\xbf\x80\x00\x00\xff\x02\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')
    fields1 = [0, 9, 1, 9, -1.0, -1.0, -1.0, -1.0, 9, 2]
    fields2 = [0, 255, 1, 255, -1.0, -1.0, -1.0, -1.0, 255, 2, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]

class Test0xbc_1(PacketTest):
    (code, subcode, fields, binary) = (0xbc, None, [0], '\xbc\x00')
    
class Test0xbc_2(PacketTest):
    (code, subcode, fields, binary) = (0xbc, None, [0, 6, 7, 3, 0, 0, 0, 2, 2, 0], '\xbc\x00\x06\x07\x03\x00\x00\x00\x02\x02\x00')

# Superpacket commands
#
class Test0x8e15(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0x15, [], '\x8e\x15')
    
class Test0x8e23(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0x23, [1], '\x8e#\x01')
    
class Test0x8e26(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0x26, [], '\x8e\x26')
    
class Test0x8e41(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0x41, [], '\x8e\x41')
    
class Test0x8e42(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0x42, [], '\x8e\x42')
    
class Test0x8e45(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0x45, [3], '\x8eE\x03')
    
class Test0x8e4a(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0x4a, [1, 2, 1, 0.10000000000000001, 0.20000000298023224], 
                                       '\x8eJ\x01\x02\x01?\xb9\x99\x99\x99\x99\x99\x9a>L\xcc\xcd')

class Test0x8e4c(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0x4c, [0xff], '\x8eL\xff')

class Test0x8e4e(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0x4e, [0x02], '\x8eN\x02')
    
class Test0x8ea0_1(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0xa0, [], '\x8e\xa0')
    
class Test0x8ea0_2(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0xa0, [0, 1.0], '\x8e\xa0\x00?\x80\x00\x00')
    
class Test0x8ea0_3(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0xa0, [1, 1000], '\x8e\xa0\x01\x00\x00\x03\xe8')
    
class Test0x8ea2(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0xa2, [2], '\x8e\xa2\x02')
    
class Test0x8ea3(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0xa3, [5], '\x8e\xa3\x05')
    
class Test0x8ea4_0(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0xa4, [0], '\x8e\xa4\x00')
    
class Test0x8ea4_1(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0xa4, [1, 1023, 604799], '\x8e\xa4\x01\x03\xff\x00\t:\x7f')
    
class Test0x8ea4_3(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0xa4, [3, 1.0, 2.0, -1, 1, 2, 3, 4, -5], 
                                       '\x8e\xa4\x03?\x80\x00\x00@\x00\x00\x00\xff\xff\x00\x00\x00\x01\x00\x02\x00\x03\x00\x04\xff\xfb')
    
class Test0x8ea5(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0xa5, [1, 2], '\x8e\xa5\x00\x01\x00\x02')

class Test0x8ea6(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0xa6, [0], '\x8e\xa6\x00')
    
class Test0x8ea8_0(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0xa8, [0, 1.0, 2.0], '\x8e\xa8\x00?\x80\x00\x00@\x00\x00\x00')
    
class Test0x8ea8_1(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0xa8, [1, 1.0, 2.0, 3.0], '\x8e\xa8\x01?\x80\x00\x00@\x00\x00\x00@@\x00\x00')
    
class Test0x8ea8_2(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0xa8, [2, 4.0, 5.0], '\x8e\xa8\x02@\x80\x00\x00@\xa0\x00\x00')
    
class Test0x8ea8_3(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0xa8, [3, 6.0], '\x8e\xa8\x03@\xc0\x00\x00')  
    
class Test0x8ea9(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0xa9, [0, 1, 1000, 2000], '\x8e\xa9\x00\x01\x00\x00\x03\xe8\x00\x00\x07\xd0')
    
class Test0x8eab(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0xab, [2], '\x8e\xab\x02')
    
class Test0x8eac(PacketTest):
    (code, subcode, fields, binary) = (0x8e, 0xac, [2], '\x8e\xac\x02')


# Superpacket reports
#
class Test0x8f15(PacketTest):
    (code, subcode, fields, binary) = (0x8f, 0x15, [-1, 1000.0, 2000.0, 3000.0, 4000.0, 5000.0], 
                                       '\x8f\x15\xff\xff@\x8f@\x00\x00\x00\x00\x00@\x9f@\x00\x00\x00\x00\x00@\xa7p\x00\x00\x00\x00\x00@\xaf@\x00\x00\x00\x00\x00@\xb3\x88\x00\x00\x00\x00\x00')

class Test0x8f23(PacketTest):
    (code, subcode, fields, binary) = (0x8f, 0x23, [1, 2, 3, 4, -37, 144, -10, 10, 20, 30, 5],
                                       '\x8f#\x00\x00\x00\x01\x00\x02\x03\x04\xff\xff\xff\xdb\x00\x00\x00\x90\xff\xff\xff\xf6\x00\n\x00\x14\x00\x1e\x00\x05')    

class Test0x8f41(PacketTest):
    # TODO: is the year really an UINT8?
    (code, subcode, fields, binary) = (0x8f, 0x41, [0, 98765, 15, 11, 20, 16, 0.0, 1],
                                       '\x8fA\x00\x00\x00\x01\x81\xcd\x0f\x0b\x14\x10\x00\x00\x00\x00\x00\x01')
    
class Test0x8f42(PacketTest):
    (code, subcode, fields, binary) = (0x8f, 0x42, [1, 2, 3, 4, 5, 6, 7, 8],
                                       '\x8fB\x01\x02\x00\x03\x00\x00\x00\x04\x00\x00\x00\x05\x00\x06\x00\x07\x00\x08')

class Test0x8f4a(PacketTest):
    (code, subcode, fields, binary) = (0x8f, 0x4a, [1, 2, 1, 0.10000000000000001, 0.20000000298023224], 
                                       '\x8fJ\x01\x02\x01?\xb9\x99\x99\x99\x99\x99\x9a>L\xcc\xcd')

class Test0x8f4e(PacketTest):
    (code, subcode, fields, binary) = (0x8f, 0x4e, [0x02], '\x8fN\x02')

class Test0x8fa0(PacketTest):
    (code, subcode, fields, binary) = (0x8f, 0xa0, [1234, 1.0, 0, 1, 2.0, 3.0],
                                       '\x8f\xa0\x00\x00\x04\xd2?\x80\x00\x00\x00\x01@\x00\x00\x00@@\x00\x00')

class Test0x8fa2(PacketTest):
    (code, subcode, fields, binary) = (0x8f, 0xa2, [2], '\x8f\xa2\x02') 

class Test0x8fa3(PacketTest):
    (code, subcode, fields, binary) = (0x8f, 0xa3, [5], '\x8f\xa3\x05')

class Test0x8fa4_0(PacketTest):
    (code, subcode, fields, binary) = (0x8f, 0xa4, [0], '\x8f\xa4\x00')
    
class Test0x8fa4_1(PacketTest):
    (code, subcode, fields, binary) = (0x8f, 0xa4, [1, 1023, 604799], '\x8f\xa4\x01\x03\xff\x00\t:\x7f')
    
class Test0x8fa4_3(PacketTest):
    (code, subcode, fields, binary) = (0x8f, 0xa4, [3, 1.0, 2.0, -1, 1, 2, 3, 4, -5], 
                                       '\x8f\xa4\x03?\x80\x00\x00@\x00\x00\x00\xff\xff\x00\x00\x00\x01\x00\x02\x00\x03\x00\x04\xff\xfb') 

class Test0x8fa5(PacketTest):
    (code, subcode, fields, binary) = (0x8f, 0xa5, [1, 2], '\x8f\xa5\x00\x01\x00\x02')
    
class Test0x8fa6(PacketTest):
    (code, subcode, fields, binary) = (0x8f, 0xa6, [0], '\x8f\xa6\x00')
    
class Test0x8fa8_0(PacketTest):
    (code, subcode, fields, binary) = (0x8f, 0xa8, [0, 1.0, 2.0], '\x8f\xa8\x00?\x80\x00\x00@\x00\x00\x00')
    
class Test0x8fa8_1(PacketTest):
    (code, subcode, fields, binary) = (0x8f, 0xa8, [1, 1.0, 2.0, 3.0], '\x8f\xa8\x01?\x80\x00\x00@\x00\x00\x00@@\x00\x00')
    
class Test0x8fa8_2(PacketTest):
    (code, subcode, fields, binary) = (0x8f, 0xa8, [2, 4.0, 5.0], '\x8f\xa8\x02@\x80\x00\x00@\xa0\x00\x00')
    
class Test0x8fa8_3(PacketTest):
    (code, subcode, fields, binary) = (0x8f, 0xa8, [3, 6.0], '\x8f\xa8\x03@\xc0\x00\x00')
    
class Test0x8fa9(PacketTest):
    (code, subcode, fields, binary) = (0x8f, 0xa9, [0, 1, 1000, 2000], '\x8f\xa9\x00\x01\x00\x00\x03\xe8\x00\x00\x07\xd0')
    
class Test0x8fab(PacketTest):
    (code, subcode, fields, binary) = (0x8f, 0xab, [1, 2, -1, 3, 4, 5, 6, 7, 8, 2015],
                                       '\x8f\xab\x00\x00\x00\x01\x00\x02\xff\xff\x03\x04\x05\x06\x07\x08\x07\xdf')

class Test0x8fac(PacketTest):
    (code, subcode, fields, binary) = (0x8f, 0xac, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11.0, 12.0, 13, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 0],
                                       '\x8f\xac\x01\x02\x03\x00\x00\x00\x04\x00\x05\x00\x06\x07\x08\t\nA0\x00\x00A@\x00\x00\x00\x00\x00\rA`\x00\x00Ap\x00\x00@0\x00\x00\x00\x00\x00\x00@1\x00\x00\x00\x00\x00\x00@2\x00\x00\x00\x00\x00\x00A\x98\x00\x00\x00\x00\x00\x00')
