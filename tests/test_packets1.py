
from nose.tools import *

from tsip.packets1 import *

class Base(object):

    def test_code(self):
        assert self.pkt.code == self.code
        assert self.pkt.code == self.pkt._code

    @raises(AttributeError)
    def test_code_readonly(self):
        self.pkt.code = -1

    def test_subcode(self):
        if hasattr(self, 'subcode'):
            assert self.pkt.subcode == self.subcode
            assert self.pkt.subcode == self.pkt._subcode

    @raises(AttributeError)
    def test_subcode_readonly(self):
        if hasattr(self, 'subcode'):
            self.pkt.subcode = -1


class Test_Packet_0x1c01(Base):
    code = 0x1c
    subcode = 0x01

    def setup(self):
        self.pkt = Packet_0x1c01()


class Test_Packet_0x1c03(Base):
    code = 0x1c
    subcode = 0x03

    def setup(self):
        self.pkt = Packet_0x1c03()


class Test_Packet_0x1c81(Base):
    code = 0x1c
    subcode = 0x81

    def setup(self):
        self.pkt = Packet_0x1c81(0, 1, 2, 3, 8, 15, 2015, 'test product')

    def test_attributes(self):
        assert self.pkt.reserved1 == 0
        assert self.pkt.major_version == 1
        assert self.pkt.minor_version == 2
        assert self.pkt.build_number == 3
        assert self.pkt.month == 8
        assert self.pkt.day == 15
        assert self.pkt.year == 2015
        assert self.pkt.product_name == 'test product'

        self.pkt.reserve1 = 100
       
        assert self.pkt.reserved1 == 0
       
       
    def test_list(self):
        assert self.pkt[0] == 0
        assert self.pkt[1] == 1
        assert self.pkt[2] == 2
        assert self.pkt[3] == 3
        assert self.pkt[4] == 8
        assert self.pkt[5] == 15
        assert self.pkt[6] == 2015
        assert self.pkt[7] == 'test product'

        self.pkt[0] = 200
       
        assert self.pkt[0] == 200


