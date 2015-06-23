

from nose.tools import *

from tsip.gps import GPS, Packet


class CyclicFileReader(object):
    """
    Crude file-like object that continues reading from the beginning
    once EOF is reached. In this test module it is used to read
    TSIP data from files over and over again.

    """

    def __init__(self, path):
        self.fp = open(path, 'rb')


    def read(self, size=1):
        """
        In this test module we only ever read a single byte
        so size is hard-coded.

        """
         
        data = self.fp.read(1)
        if data == '':
            self.fp.seek(0)
            data = self.fp.read(1)
               
        return data


    def close(self):
        self.fp.close()


class _CapturesBase():

    def setup(self):
        self.conn = open(self.filename, 'rb')
        self.gps = GPS(self.conn)

    def teardown(self):
        self.conn.close()

    def test_packets(self):
        for packet in self.gps:
            assert isinstance(packet, Packet)
        


class TestThunderbolt(_CapturesBase):
    filename = 'tests/thunderbolt.tsip'

