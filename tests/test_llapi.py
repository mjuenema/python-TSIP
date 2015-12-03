"""
Tests for tsip.llapi.

MJ, 19-Nov-2015

"""

TSIPFILE = 'thunderbolt.tsip'

import os.path

from nose.tools import *

from tsip.config import *
from tsip.llapi import *

class TestIsFramed(object):
    
    def test_isframed(self):
        assert is_framed(CHR_DLE + CHR_DLE + CHR_ETX) is True
        assert is_framed(CHR_DLE + 'payload' + CHR_DLE + CHR_ETX) is True
        
        
class TestFrame(object):
    
    def test_frame(self):
        assert frame('payload') == CHR_DLE + 'payload' + CHR_DLE + CHR_ETX
        
    def test_unframe(self): 
        assert unframe(CHR_DLE + 'payload' + CHR_DLE + CHR_ETX) == 'payload'
    
    @raises(ValueError)
    def test_frame_valueerror(self):
        frame(CHR_DLE + 'payload' + CHR_DLE + CHR_ETX)
        
    @raises(ValueError)
    def test_unframe_valueerror(self):
        unframe('payload')
        

class TestStuff(object):
    
    def test_stuff(self):
        assert stuff('payload') == 'payload'
        assert stuff(CHR_DLE + 'payload') == CHR_DLE + CHR_DLE + 'payload'
        assert stuff(CHR_DLE + 'payload' + CHR_DLE) == CHR_DLE + CHR_DLE + 'payload' + CHR_DLE + CHR_DLE
        assert stuff(CHR_DLE + CHR_DLE + 'payload') == CHR_DLE + CHR_DLE + CHR_DLE + CHR_DLE + 'payload'
        
    def test_unstuff(self):
        assert unstuff('payload') == 'payload'
        assert unstuff(CHR_DLE + CHR_DLE + 'payload') == CHR_DLE + 'payload'
        assert unstuff(CHR_DLE + CHR_DLE + 'payload' + CHR_DLE + CHR_DLE) == CHR_DLE + 'payload' + CHR_DLE
        assert unstuff(CHR_DLE + CHR_DLE + CHR_DLE + CHR_DLE + 'payload') == CHR_DLE + CHR_DLE + 'payload'
        
    @raises(ValueError)
    def test_stuff_valueerror(self):
        stuff(CHR_DLE + 'payload' + CHR_DLE + CHR_ETX)
        
    @raises(ValueError)
    def test_unstuff_valueerror(self):
        unstuff(CHR_DLE + 'payload' + CHR_DLE + CHR_ETX)
        
        
class TestGPS(object):
    
    def setup(self):
        try:
            self.conn = open(TSIPFILE, 'rb')
        except IOError:
            self.conn = open(os.path.join('tests', TSIPFILE), 'rb')
            
        self.gps_ = gps(self.conn)
        
    def teardown(self):
        self.conn.close()
        
    def test_init(self):
        assert isinstance(self.gps_, gps)
        assert self.gps_.conn == self.conn
        
#    def test_next(self):
#        packet = self.gps_.next()
#        assert packet.startswith(CHR_DLE)
#        assert packet.endswith(CHR_DLE + CHR_ETX)
#        packet = self.gps_.next()
#        assert packet.startswith(CHR_DLE)
#        assert packet.endswith(CHR_DLE + CHR_ETX)
#        packet = self.gps_.next()
#        assert packet.startswith(CHR_DLE)
#        assert packet.endswith(CHR_DLE + CHR_ETX)

    def test_iter(self):
        for packet in self.gps_:
            assert packet.startswith(CHR_DLE)
            assert packet.endswith(CHR_DLE + CHR_ETX)
            
#    def test_unframe(self):
#        for packet in self.gps_:
#            data = unframe(packet)
#            # This test is actually brittle as `data` could start 
#            # with DLE. It does not with the TSIP capture used here.
#            assert not data.startswith(CHR_DLE)
#            assert not data.endswith(CHR_DLE + CHR_ETX)
