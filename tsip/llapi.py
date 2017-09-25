# -*- coding: utf-8 -*-
"""
Low-level API.

"""

from tsip.config import *


def is_framed(packet):
    """
    Check whether a packet contains leading DLE and trailing DLE/ETX.

    :param packet: TSIP packet with or without leading DLE and trailing DLE/ETX.
    :type packet: Binary string.
    :returns: ``True`` if leading DLE and trailing DLE/ETX are still present,
        ``False`` otherwise.

    """

    return packet[0] == CHR_DLE and packet[-2] == CHR_DLE and packet[-1] == CHR_ETX


def frame(data):
    """
    Add leading DLE and trailing DLE/ETX to data.

    :param data: TSIP data without leading DLE and trailing DLE/ETX.
    :type data: Binary string.
    :return: TSIP data with leading DLE and trailing DLE/ETX added.
    :raise: ``ValueError`` if `data` already starts with DLE and ends in DLE/ETX.

    """

    if is_framed(data):
        raise ValueError('data contains leading DLE and trailing DLE/ETX')
    else:
        return CHR_DLE + data + CHR_DLE + CHR_ETX


def unframe(packet):
    """
    Strip leading DLE and trailing DLE/ETX from packet.

    :param packet: TSIP packet with leading DLE and trailing DLE/ETX.
    :type packet: Binary string.
    :return: TSIP packet with leading DLE and trailing DLE/ETX removed.
    :raise: ``ValueError`` if `packet` does not start with DLE and end in DLE/ETX.


    """

    if is_framed(packet):
        return packet.lstrip(CHR_DLE).rstrip(CHR_ETX).rstrip(CHR_DLE)
    else:
        raise ValueError('packet does not contain leading DLE and trailing DLE/ETX')


def stuff(packet):
    """
    Add byte stuffing to TSIP packet.
    :param packet: TSIP packet with byte stuffing. The packet must already
        have been stripped or `ValueError` will be raised.
    :type packet: Binary string.
    :return: Packet with byte stuffing.

    """

    if is_framed(packet):
        raise ValueError('packet contains leading DLE and trailing DLE/ETX')
    else:
        return packet.replace(CHR_DLE, CHR_DLE + CHR_DLE)



def unstuff(packet):
    """
    Remove byte stuffing from a TSIP packet.

    :param packet: TSIP packet with byte stuffing. The packet must already
        have been stripped or `ValueError` will be raised.
    :type packet: Binary string.
    :return: Packet without byte stuffing.

    """

    if is_framed(packet):
        raise ValueError('packet contains leading DLE and trailing DLE/ETX')
    else:
        return packet.replace(CHR_DLE + CHR_DLE, CHR_DLE)


class gps(object):

    def __init__(self, conn):
        self.conn = conn

    def __iter__(self):
        return self

    def read(self):

        packet = ''
        dle_count = 0

        last_b = None
        while True:
            b = self.conn.read(1)

            if len(b) == 0:
                return None

            packet += chr(ord(b))    # Python 3 work-around

            if b == CHR_DLE:
                dle_count += 1
            elif b == CHR_ETX and last_b == CHR_DLE and (dle_count % 2) == 0:    # even, because leading DLE is counted!
                return packet
            else:
                pass

            last_b = b


    def next(self):
        packet = self.read()

        if packet is None:
            raise StopIteration()
        else:
            return packet

    def __next__(self):
        return self.next()


    def write(self, packet):
        """

           :param packet: A complete TSIP packet with byte
                stuffing and framing applied.

        """

        self.conn.write(packet)
