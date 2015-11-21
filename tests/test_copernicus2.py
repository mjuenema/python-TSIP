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

import signal
import time

import serial

from nose.tools import *
from nose.plugins.attrib import attr

from tsip.hlapi import *


def sigalrm_handler(s, f):
    raise Exception('timeout expecting packet')
signal.signal(signal.SIGALRM, sigalrm_handler)


@attr(gps='copernicus2')
class TestCopernicus(object):
    def setup(self):
        self.conn = serial.Serial(PORT)
        self.conn.baudrate = BAUDRATE
        self.gps = GPS(self.conn)
        
    def send_expect(self, packet, code=None, timeout=5):
        if packet:
            self.gps.write(packet)
        
        signal.alarm(timeout)
        
        if code:
            while True:
                packet = self.gps.read()
                if packet.code == code:
                    signal.alarm(0)
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
        assert isinstance(report[1], types.IntType)  # major version
        assert isinstance(report[2], types.IntType)  # minor version
        assert isinstance(report[3], types.IntType)  # build number
        assert 1 <= report[4] <= 12                  # build month
        assert 1 <= report[5] <= 31                  # build day
        assert report[6] >= 2000                     # build year
        assert report[7] == 'Copernicus II Receiver' 
        
    def test_0x1c03_0x1c83(self):
        command = Packet(0x1c, 0x03)
        report = self.send_expect(command, 0x1c)
        assert report.code == 0x1c
        assert report.subcode == 0x83
        assert report[0] > 1000000000
        assert 1 <= report[1] <= 31
        assert 1 <= report[2] <= 12 
        assert report[3] >= 2000                    
        assert 0 <= report[4] <= 24
        assert report[5] > 1000
        assert report[6] == 'Copernicus II Receiver'
        
#     def test_0x1e_0x4b(self):
#         command = Packet(0x1e, 0x4b)
#         report = self.send_expect(command, 0x4b)
#         assert report.code == 0x4b
#         time.sleep(5)   # wait until reset
#       
#     def test_0x1e_0x45(self):
#         command = Packet(0x1e, 0x4b)
#         report = self.send_expect(command, 0x45)
#         assert report.code == 0x45
#         time.sleep(5)   # wait until reset
# #         
#     def test_0x1e_0x46(self):
#         command = Packet(0x1e, 0x4b)
#         report = self.send_expect(command, 0x46)
#         assert report.code == 0x46
#         time.sleep(5)   # wait until reset
        
    def test_0x1f_0x45(self):
        command = Packet(0x1f)
        report = self.send_expect(command, 0x45)
        
    def test_0x21_0x41(self):
        command = Packet(0x21)
        report = self.send_expect(command, 0x41)
        assert 0.0 <= report[0] <= 604801
        assert report[1] >= 1871
        assert report[2] >= 17.0    # breaks, should we get a negative leap second!!!

# TODO: 0x23

    def test_0x24_0x6d(self):
        command = Packet(0x24)
        report = self.send_expect(command, 0x6d)
        assert report[0] & 0b00000111 in [3, 4]
        assert (report[0] & 0b1111000) >> 4 == len(report.fields) - 5
    
#     def test_0x25_0x4b(self):
#         command = Packet(0x25)
#         report = self.send_expect(command, 0x4b)
#         time.sleep(5)   # wait until reset
#         
#     def test_0x25_0x45(self):
#         command = Packet(0x25)
#         report = self.send_expect(command, 0x45)
#         time.sleep(5)   # wait until reset
#         
#     def test_0x25_0x46(self):
#         command = Packet(0x25)
#         report = self.send_expect(command, 0x46)
#         time.sleep(5)   # wait until reset
        
#     def test_0x26_0x45(self):
#         command = Packet(0x26)
#         report = self.send_expect(command, 0x45)
        
    def test_0x26_0x46(self):
        command = Packet(0x26)
        report = self.send_expect(command, 0x46)
        
    def test_0x27_0x47(self):
        command = Packet(0x27)
        report = self.send_expect(command, 0x47)
        assert report[0] == (len(report.fields)-1)/2
     
# TODO: 0x2b

    def test_0x2d_0x4d(self):
        command = Packet(0x2d)
        report = self.send_expect(command, 0x4d)

# TODO: 0x2e

