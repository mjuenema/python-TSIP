

from nose.tools import *
from tsip.packets import *
import struct
import types


class TestPackets():

    def test_type(self):
        for (k, v) in PACKETS.items():
            (f, a, d) = v
            assert type(f) in [types.StringType, types.FunctionType]
            assert isinstance(a, types.ListType)
            assert isinstance(d, types.StringType)

            if isinstance(f, types.StringType):
                assert struct.Struct(f).size >= 0
