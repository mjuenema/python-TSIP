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
        assert is_framed(bDLE + bDLE + bETX) is True
        assert is_framed(bDLE + b'payload' + bDLE + bETX) is True


class TestFrame(object):

    def test_frame(self):
        assert frame(b'payload') == bDLE + b'payload' + bDLE + bETX

    def test_unframe(self):
        assert unframe(bDLE + b'payload' + bDLE + bETX) == b'payload'

    @raises(ValueError)
    def test_frame_valueerror(self):
        frame(bDLE + b'payload' + bDLE + bETX)

    @raises(ValueError)
    def test_unframe_valueerror(self):
        unframe(b'payload')


class TestStuff(object):

    def test_stuff(self):
        assert stuff(b'payload') == b'payload'
        assert stuff(bDLE + b'payload') == bDLE + bDLE + b'payload'
        assert stuff(bDLE + b'payload' + bDLE) == bDLE + bDLE + b'payload' + bDLE + bDLE
        assert stuff(bDLE + bDLE + b'payload') == bDLE + bDLE + bDLE + bDLE + b'payload'

    def test_unstuff(self):
        assert unstuff(b'payload') == b'payload'
        assert unstuff(bDLE + bDLE + b'payload') == bDLE + b'payload'
        assert unstuff(bDLE + bDLE + b'payload' + bDLE + bDLE) == bDLE + b'payload' + bDLE
        assert unstuff(bDLE + bDLE + bDLE + bDLE + b'payload') == bDLE + bDLE + b'payload'

    @raises(ValueError)
    def test_stuff_valueerror(self):
        stuff(bDLE + b'payload' + bDLE + bETX)

    @raises(ValueError)
    def test_unstuff_valueerror(self):
        unstuff(bDLE + b'payload' + bDLE + bETX)


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
#        assert packet.startswith(bDLE)
#        assert packet.endswith(bDLE + bETX)
#        packet = self.gps_.next()
#        assert packet.startswith(bDLE)
#        assert packet.endswith(bDLE + bETX)
#        packet = self.gps_.next()
#        assert packet.startswith(bDLE)
#        assert packet.endswith(bDLE + bETX)

    def test_iter(self):
        for packet in self.gps_:
            assert packet.startswith(bDLE)
            assert packet.endswith(bDLE + bETX)

#    def test_unframe(self):
#        for packet in self.gps_:
#            data = unframe(packet)
#            # This test is actually brittle as `data` could start
#            # with DLE. It does not with the TSIP capture used here.
#            assert not data.startswith(bDLE)
#            assert not data.endswith(bDLE + bETX)
