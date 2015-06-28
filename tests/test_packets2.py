
from nose.tools import *

from tsip.packets2 import *


class TestCommand1c(object):

    def test_subcode_1(self):
        p = Command_1c(1)
        assert p.code == 0x1c
        assert p.values == [1]
        assert p[0] == 1
        assert p.packet == struct.pack('>BB', 0x1c, 1)

    def test_subcode_3(self):
        p = Command_1c(3)
        assert p.code == 0x1c
        assert p.values == [3]
        assert p[0] == 3
        assert p.packet == struct.pack('>BB', 0x1c, )

    @raises(ValueError)
    def test_valueerror(self):
        p = Command_1c(99)
