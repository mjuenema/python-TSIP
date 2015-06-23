

from nose.tools import *
from tsip.packets import *
import struct
import types


class TestFormats():

    def test_struct(self):
        for (k, f) in FORMATS.items():
            if isinstance(f, types.StringType):
                assert struct.Struct(f).size >= 0

                if len(f) > 0:
                    assert f[0] == '>'	# big-endian
