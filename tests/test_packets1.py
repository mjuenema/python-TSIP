
from nose.tools import *

from tsip.packets1 import *


class TestCommand1c(object):

    def test_subcode_1(self):
        p = Command_1c(1)
        assert p.code == 0x1c
        assert p._values == [1]
        assert p[0] == 1
        assert p._packet == struct.pack('>BB', 0x1c, 1)
        p[0] = 2
        assert p[0] == 2
        assert p._packet == struct.pack('>BB', 0x1c, 2)
        p[0] = 1
        assert p[0] == 1
        assert p._packet == struct.pack('>BB', 0x1c, 1)

    def test_subcode_3(self):
        p = Command_1c(3)
        assert p.code == 0x1c
        assert p._values == [3]
        assert p[0] == 3
        assert p._packet == struct.pack('>BB', 0x1c, 3)
        p[0] = 2
        assert p[0] == 2
        assert p._packet == struct.pack('>BB', 0x1c, 2)
        p[0] = 3
        assert p[0] == 3
        assert p._packet == struct.pack('>BB', 0x1c, 3)

#    @raises(IndexError)
#    def test_indexerror(self):
#        p = Command_1c(1)
#        p[1] = None


class TestCommand1e(object):

    def tests(self):
        p = Command_1e(0x4b)
        assert p.code == 0x1e
        assert p._values == [0x4b]
        assert len(p._values) == 1
        assert p[0] == 0x4b

#    @raises(IndexError)
#    def test_indexerror(self):
#        p = Command_1e(0x4b)
#        p[0] = None

class TestCommand1f(object):

    def tests(self):
        p = Command_1f()
        assert p.code == 0x1f
        assert p._values == []
        assert len(p._values) == 0
