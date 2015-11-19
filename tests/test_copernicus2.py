"""
Test with a connected Trimble Copernicus II GPS.

The tests verify whether the high-level API (hlapi)
can be used to communicate with a real Trimble Copernicus II GPS.

These tests require ``pyserial`` to be installed and 
are only run when ``nosetools`` is called like this::

  nosetools -a 'gps=copernicus2' ...
  
Edit this script and set the global variables PORT and
BAUDRATE as needed!

MJ, 19-Nov-2015

"""

PORT = '/dev/ttyAMA0'
BAUDRATE = 38400

import serial

from nose.tools import *
from nose.plugins.attrib import attr

from tsip.hlapi import *



@attr(gps='copernicus2')
class TestCopernicus(object):
    def setup(self):
        self.conn = serial.Serial(PORT)
        self.conn.baudrate = BAUDRATE
        self.gps = GPS(self.conn)
        
    def send_expect(self, packet, code, timeout=5):
        self.gps.write(packet)
        
        while True:
            packet = self.gps.read()
            if packet.code == code:
                return packet
    
    def test_read(self):
        packet = self.gps.read()
        assert isinstance(packet, Packet)
        
        if packet.code in PACKETS_WITH_SUBCODE:
            assert packet.subcode is not None
        else:
            assert packet.subcode is None
            
    def test_0x1c01_0x1c81(self):
        command = Packet(0x1c, 0x01)
        report = self.send_expect(command, 0x1c)
        assert report.code == 0x1c
        assert report.subcode == 0x81
        assert isinstance(report.fields[1], types.IntType)  # major version
        assert isinstance(report.fields[2], types.IntType)  # minor version
        assert isinstance(report.fields[3], types.IntType)  # build number
        assert 1 <= report.fields[4] <= 12                  # build month
        assert 1 <= report.fields[5] <= 31                  # build day
        assert report.fields[6] >= 2000                     # build year
        assert report.fields[7] == 'Copernicus II Receiver' 
    
    




