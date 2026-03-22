"""
Tests for tsip.llapi.

MJ, 19-Nov-2015

"""

TSIPFILE = 'thunderbolt.tsip'

import os.path

from nose.tools import *

from tsip.config import *
from tsip.llapi import *

bID = b'\x42' # just a valid single-byte ID

class TestIsFramed(object):

    def test_isframed(self):
        # Following TSIP Packet Structure from ICM SMT 360™ & RES SMT 360™ USER GUIDE.
        # <DLE DLE ETX> is neither a valid framed packet (ID at [1] can't be DLE and can't be empty)
        # nor a valid unframed & unstuffed packet (ID at [0] can't be DLE, once again).
        assert is_framed(bDLE + bDLE + bETX) is False
        assert is_framed(bDLE + bDLE + bDLE + bETX) is False
        assert is_framed(bDLE + bETX + bDLE + bETX) is False

        # Boring good packets:
        assert is_framed(bDLE + bID + bDLE + bETX) is True
        assert is_framed(bDLE + b'payload' + bDLE + bETX) is True

        # define API for None
        assert is_framed(None) is False

class TestFrame(object):

    def test_frame(self):
        assert frame(b'payload') == bDLE + b'payload' + bDLE + bETX

    def test_unframe(self):
        assert unframe(bDLE + b'payload' + bDLE + bETX) == b'payload'
        assert unframe(bDLE + b'pay' + bDLE_DLE + bDLE_ETX) == b'pay' + bDLE_DLE

    def test_encode(self):
        assert frame(stuff(b'payload')) == bDLE + b'payload' + bDLE + bETX
        assert frame(stuff(b'pay' + bDLE)) == bDLE + b'pay' + bDLE_DLE + bDLE_ETX
        assert frame(stuff(b'pay' + bDLE + bDLE)) == bDLE + b'pay' + bDLE_DLE + bDLE_DLE + bDLE_ETX

    def test_decode(self):
        assert unstuff(unframe(b'\x10pay\x10\x10\x10\x03')) == b'pay\x10'
        assert unstuff(unframe(b'\x10pay\x10\x10\x10\x10\x10\x03')) == b'pay\x10\x10'
        assert unstuff(unframe(b'\x10pa\x10\x10y\x10\x10\x10\x03')) == b'pa\x10y\x10'
        assert unstuff(unframe(b'\x10p\x10\x10ay\x10\x10\x10\x03')) == b'p\x10ay\x10'

    @raises(ValueError)
    def test_frame_nonstuffed_odd(self):
        assert frame(b'pay\x10')

    @raises(ValueError)
    def test_frame_nonstuffed_even(self):
        assert frame(b'pa\x10y\x10')

    @raises(ValueError)
    def test_frame_DLE(self):
        assert frame(bDLE + b'payload')

    @raises(ValueError)
    def test_frame_ETX(self):
        assert frame(bETX + b'payload')

    @raises(ValueError)
    def test_frame_framed(self):
        frame(bDLE + b'payload' + bDLE + bETX)

    @raises(ValueError)
    def test_unframe_valueerror(self):
        unframe(b'payload')

    @raises(ValueError)
    def test_unframe_empty_packet(self):
        unframe(bDLE + bDLE_ETX)

class TestStuff(object):

    def test_stuff(self):
        assert stuff(b'payload') == b'payload'
        assert stuff(bID + bDLE + b'payload') == bID + bDLE_DLE + b'payload'
        assert stuff(bID + bDLE + b'payload' + bDLE) == bID + bDLE_DLE + b'payload' + bDLE_DLE
        assert stuff(bID + bDLE + bDLE + b'payload') == bID + bDLE_DLE + bDLE_DLE + b'payload'

    def test_unstuff(self):
        assert unstuff(b'payload') == b'payload'
        assert unstuff(bID + bDLE_DLE + b'payload') == bID + bDLE + b'payload'
        assert unstuff(bID + bDLE_DLE + b'payload' + bDLE + bDLE) == bID + bDLE + b'payload' + bDLE
        assert unstuff(bID + bDLE_DLE + bDLE_DLE + b'payload') == bID + bDLE + bDLE + b'payload'

    @raises(ValueError)
    def test_stuff_valueerror(self):
        stuff(bDLE + b'payload' + bDLE + bETX)

    @raises(ValueError)
    def test_stuff_id_eq_dle(self):
        stuff(bDLE + b'payload')

    @raises(ValueError)
    def test_unstuff_valueerror(self):
        unstuff(bDLE + b'payload' + bDLE + bETX)

    @raises(ValueError)
    def test_unstuff_not_stuffed(self):
        unstuff(bID + bDLE + b'payload' )


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

def setup_tsipfile(fname):
    if os.path.isfile(fname):
        return fname
    fname = os.path.join('tests', fname)
    assert os.path.isfile(fname)
    return fname

KNOWN_DUMPS = (
    ('thunderbolt.tsip', 211),
    ('copernicus2.tsip', 2478),
)

def test_gps_next():
    for fname, expected_count in KNOWN_DUMPS:
        conn = open(setup_tsipfile(fname), 'rb')
        gps_ = gps(conn)
        count = 0
        for packet in iter(gps_.next, None):
            assert packet.startswith(bDLE)
            assert packet.endswith(bDLE_ETX)
            count += 1
        assert count == expected_count

def test_gps_iter():
    for fname, expected_count in KNOWN_DUMPS:
        conn = open(setup_tsipfile(fname), 'rb')
        gps_ = gps(conn)
        count = 0
        for packet in gps_:
            assert packet.startswith(bDLE)
            assert packet.endswith(bDLE + bETX)
            count += 1
        assert count == expected_count

#    def test_unframe(self):
#        for packet in self.gps_:
#            data = unframe(packet)
#            # This test is actually brittle as `data` could start
#            # with DLE. It does not with the TSIP capture used here.
#            assert not data.startswith(bDLE)
#            assert not data.endswith(bDLE + bETX)
