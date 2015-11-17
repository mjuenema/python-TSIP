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


def frame(packet):
    """
    Add leading DLE and trailing DLE/ETX to packet. 

    :param packet: TSIP packet without leading DLE and trailing DLE/ETX.
    :type packet: Binary string.
    :return: TSIP packet with leading DLE and trailing DLE/ETX added.

    If the packet already starts with DLE and ends in DLE/ETX then the 
    packet is returned unchanged.

    """

    if is_framed(packet):
        return packet
    else:
        return CHR_DLE + packet + CHR_DLE + CHR_ETX


def unframe(packet):
    """
    Strip leading DLE and trailing DLE/ETX from packet. 

    :param packet: TSIP packet with leading DLE and trailing DLE/ETX.
    :type packet: Binary string.
    :return: TSIP packet with leading DLE and trailing DLE/ETX removed.

    If the packet does not start with DLE _and_ end with DLE/ETX it will be
    returned unchanged. It should therefore be reasonably safe to "strip" a
    packet twice. A packet must be stripped first before it is "unstuffed".

    The `frame()` function is the opposite to `strip()`. 

    """

    if is_framed(packet):
        return packet.lstrip(CHR_DLE).rstrip(CHR_ETX).rstrip(CHR_DLE)
    else:
        return packet


def stuff(packet):
    """
    Add byte stuffing to TSIP packet.
    :param packet: TSIP packet with byte stuffing. The packet must already
        have been stripped or `ValueError` will be raised.
    :type packet: Binary string.
    :return: Packet with byte stuffing.

    """

    if is_framed(packet):
        return packet.replace(CHR_DLE + CHR_DLE, CHR_DLE)
    else:
        raise ValueError('packet contains leading DLE and trailing DLE/ETX')


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

    def __init__(self, reader):
        self.reader = reader

    def __iter__(self):
        return self

    def read(self):
    
        packet = ''
        dle_count = 0

        while True:
            b = self.reader.read(1)

            if b == '':
                return None

            packet += b

            if b == CHR_DLE:
                dle_count += 1
            elif b == CHR_ETX and (dle_count % 2) == 0:    # even, because leading DLE is counted!
                return unstuff(unframe(packet))
                packet = ''
                dle_count = 0
            else:
                pass


    def next(self):
        packet = self.read()

        if packet is None:
            raise StopIteration()
        else:
            return packet

