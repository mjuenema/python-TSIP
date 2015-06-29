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

class TestGps_Unknown(_TestGps):
    tsip = struct.pack('>BBcBB', DLE, 0 , 'Y', DLE, ETX)

    def test_read(self):
        packet = self.gps.read()
        assert packet.code == 0
        assert packet._format is None
        assert packet._values == []
        assert len(packet) == 0

    def test_iter(self):
        packets = list(self.gps)
        assert len(packets) == 1
        assert packets[0].code == 0
        assert packets[0]._format is None
        assert packets[0]._values == []
        assert len(packets[0]) == 0


class TestGps_0x4e_Y(_TestGps):
    tsip = struct.pack('>BBcBB', DLE, ID , 'Y', DLE, ETX)

    def test_read(self):
        packet = self.gps.read()
        assert packet.code == ID
        assert packet[0] == 'Y'
        assert len(packet) == 1

    def test_iter(self):
        packets = list(self.gps)
        assert len(packets) == 1
        assert packets[0].code == ID
        assert packets[0][0] == 'Y'
        assert len(packets[0]) == 1


class TestGps_0x4e_Y_0x4e_N(_TestGps):
    tsip = struct.pack('>BBcBB', DLE, ID , 'Y', DLE, ETX) +  struct.pack('>BBcBB', DLE, ID , 'N', DLE, ETX)

    def test_read(self):
        packet = self.gps.read()
        assert packet.code == ID
        assert packet[0] == 'Y'
        assert len(packet) == 1

        packet = self.gps.read()
        assert packet.code == ID
        assert packet[0] == 'N'
        assert len(packet) == 1


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
        assert len(packet) == 1

        packet = self.gps.read()
        assert packet.code == ID
        assert packet[0] == DLE_STRUCT
        assert len(packet) == 1


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
        assert len(packet) == 1

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
        assert len(packet) == 1

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

# -------------------------------------

class TestPacket(object):

    def test_packet_formats(self):
        for (code, format) in FORMATS.items():
            packet = Packet(code)
            assert packet.code == code
            assert type(packet._format) in [types.StringType, types.FunctionType, types.NoneType]
           
#            if isinstance(packet._format, types.StringType): 
#                assert struct.Struct(packet._format).size >= 0
#
#                assert isinstance(struct.pack(packet._format, *packet._values), types.StringType)
#
#                if len(packet._format) > 0:
#                    assert packet._format[0] == '>'  # big-endian


    def test_packet_0x4e_Y(self):
        packet = Packet(0x4e, 'Y')
        assert packet.code == 0x4e
        assert packet[0] == 'Y'
        assert packet._format == '>c'
        assert packet._values[0] == 'Y'
        assert len(packet._values) == 1
        assert len(packet) == 1
        assert packet.format() == struct.pack('>Bc', 0x4e, 'Y')



        
 


