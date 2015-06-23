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
from tsip.constants import DLE, ETX



class _TestGps(object):

    def setup(self):
        d = stringio.StringIO(self.tsip)
        self.gps = GPS(d)

#    def test_next(self):
#        packet = ''
#        try:
#            packet = self.gps.next()
#        except StopIteration:
#            pass
#
#        raise

#        assert packet == self.expected_next

    def test_read(self):
        try:
            packet = self.gps.read()
            assert packet.id == ID
            #assert packet[0] == 'Y'
        except EOFError:
            assert self.expected_read == EOFError


#    def test_iter(self):
#        packets = list(self.gps)
#        for packet in self.gps:
#            packets.append(packet)
#       
#        if packets:
#            assert packets[0].id == ID


class TestGps_0x4e_Y(_TestGps):
    tsip = struct.pack('>BBcBB', DLE, ID , 'Y', DLE, ETX)
#    expected_read = expected_next = chr(ID) + 'Y'
#    expected_iter = [chr(ID) + 'Y']


class TestGps_0x4e_DLE(_TestGps):
    tsip = struct.pack('>BBBBBB', DLE, ID , DLE, DLE, DLE, ETX)
#    expected_read = expected_next = chr(ID) + chr(DLE)
#    expected_iter = [chr(ID) + chr(DLE)]


class TestGpsError1(_TestGps):
    tsip = struct.pack('>cBB', 'Y', DLE, ETX)
    expected_read = EOFError
    expected_iter = []


class TestGpsError2(_TestGps):
    tsip = struct.pack('>BcB', DLE, 'Y', ETX)
    expected_read = EOFError
    expected_iter = []


class TestGpsError3(_TestGps):
    tsip = struct.pack('>BcB', DLE, 'Y', DLE)
    expected_read = EOFError
    expected_iter = []


# -------------------------------------

class TestPacket(object):

    def test_packet_formats(self):
        for (id, format) in FORMATS.items():
            packet = Packet(id)
            assert packet.id == id
           
            if isinstance(packet._format, types.StringType): 
                assert struct.Struct(packet._format).size >= 0

                assert isinstance(struct.pack(packet._format, *packet._values), types.StringType)

                if len(packet._format) > 0:
                    assert packet._format[0] == '>'  # big-endian



        
 


