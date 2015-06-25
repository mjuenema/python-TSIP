"""
Tests for the tsip.gps module.

"""

ID = 0x4e
"""TSIP Packet 0x4e (Set GPS time report) is abused for testing as
it conveniently contains just a single character (normally Y or N)."""


from nose.tools import *
import StringIO as stringio
import types
import struct

from tsip.gps import GPS, Packet
from tsip.packets import FORMATS, DATUMS
from tsip.constants import DLE, DLE_STRUCT, ETX, ETX_STRUCT



class _TestGps(object):

    def setup(self):
        d = stringio.StringIO(self.tsip)
        self.gps = GPS(d)


class TestGps_0x4e_Y(_TestGps):
    tsip = struct.pack('>BBcBB', DLE, ID , 'Y', DLE, ETX)

    def test_read(self):
        packet = self.gps.read()
        assert packet.code == ID
        assert packet[0] == 'Y'

    def test_iter(self):
        packets = list(self.gps)
        assert len(packets) == 1
        assert packets[0].code == ID
        assert packets[0][0] == 'Y'


class TestGps_0x4e_Y_0x4e_N(_TestGps):
    tsip = struct.pack('>BBcBB', DLE, ID , 'Y', DLE, ETX) +  struct.pack('>BBcBB', DLE, ID , 'N', DLE, ETX)

    def test_read(self):
        packet = self.gps.read()
        assert packet.code == ID
        assert packet[0] == 'Y'

        packet = self.gps.read()
        assert packet.code == ID
        assert packet[0] == 'N'


    def test_iter(self):
        packets = list(self.gps)
        assert len(packets) == 2
        assert packets[0].code == ID
        packets[0][0] == 'Y'
        assert packets[1].code == ID
        packets[1][0] == 'N'


class TestGps_0x4e_Y_0x4e_DLE(_TestGps):
    tsip = struct.pack('>BBcBB', DLE, ID , 'Y', DLE, ETX) +  struct.pack('>BBBBBB', DLE, ID , DLE, DLE, DLE, ETX)

    def test_read(self):
        packet = self.gps.read()
        assert packet.code == ID
        assert packet[0] == 'Y'

        packet = self.gps.read()
        assert packet.code == ID
        assert packet[0] == DLE_STRUCT


    def test_iter(self):
        packets = list(self.gps)
        assert len(packets) == 2
        assert packets[0].code == ID
        packets[0][0] == 'Y'
        assert packets[1].code == ID
        packets[1][0] == DLE_STRUCT


class TestGps_0x4e_DLE(_TestGps):
    tsip = struct.pack('>BBBBBB', DLE, ID , DLE, DLE, DLE, ETX)

    def test_read(self):
        packet = self.gps.read()
        assert packet.code == ID
        assert packet[0] == DLE_STRUCT

    def test_iter(self):
        packets = list(self.gps)
        assert len(packets) == 1
        assert packets[0].code == ID
        assert packets[0][0] == DLE_STRUCT


class TestGps_Incomple_and_0x4e_DLE(_TestGps):
    tsip = struct.pack('>cBBBBBB', 'x', DLE, ID , DLE, DLE, DLE, ETX)

    def test_read(self):
        packet = self.gps.read()
        assert packet.code == ID
        assert packet[0] == DLE_STRUCT

    def test_iter(self):
        packets = list(self.gps)
        assert len(packets) == 1
        assert packets[0].code == ID
        assert packets[0][0] == DLE_STRUCT


class TestGps_0x4e_DLE_and_Incomplete(_TestGps):
    tsip = struct.pack('>BBBBBBc', DLE, ID , DLE, DLE, DLE, ETX, 'x')

    def test_read(self):
        packet = self.gps.read()
        assert packet.code == ID
        assert packet[0] == DLE_STRUCT

    def test_iter(self):
        packets = list(self.gps)
        assert len(packets) == 1
        assert packets[0].code == ID
        assert packets[0][0] == DLE_STRUCT


class TestGpsError1(_TestGps):
    tsip = struct.pack('>cBB', 'Y', DLE, ETX)

    @raises(EOFError)
    def test_read(self):
        packet = self.gps.read()

    def test_iter(self):
        packets = list(self.gps)
        assert packets == []



class TestGpsError2(_TestGps):
    tsip = struct.pack('>BcB', DLE, 'Y', ETX)

    @raises(EOFError)
    def test_read(self):
        packet = self.gps.read()

    def test_iter(self):
        packets = list(self.gps)
        assert packets == []


class TestGpsError3(_TestGps):
    tsip = struct.pack('>BcB', DLE, 'Y', DLE)


    @raises(EOFError)
    def test_read(self):
        packet = self.gps.read()

    def test_iter(self):
        packets = list(self.gps)
        assert packets == []

# -------------------------------------

#class TestPacket(object):
#
#    def test_packet_formats(self):
#        for (code, format) in FORMATS.items():
#            packet = Packet(code)
#            assert packet.code == code
#           
#            if isinstance(packet._format, types.StringType): 
#                assert struct.Struct(packet._format).size >= 0
#
#                assert isinstance(struct.pack(packet._format, *packet._values), types.StringType)
#
#                if len(packet._format) > 0:
#                    assert packet._format[0] == '>'  # big-endian



        
 


