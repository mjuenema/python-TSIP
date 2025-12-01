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

    if packet == None or len(packet) < 3:
        return False
    else:
        return packet[0] == DLE and packet[-2] == DLE and packet[-1] == ETX


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
        return bDLE + data + bDLE + bETX


def unframe(packet):
    """
    Strip leading DLE and trailing DLE/ETX from packet.

    :param packet: TSIP packet with leading DLE and trailing DLE/ETX.
    :type packet: Binary string.
    :return: TSIP packet with leading DLE and trailing DLE/ETX removed.
    :raise: ``ValueError`` if `packet` does not start with DLE and end in DLE/ETX.


    """

    if is_framed(packet):
        return packet.lstrip(bDLE).rstrip(bETX).rstrip(bDLE)
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
        return packet.replace(bDLE, bDLE + bDLE)



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
        return packet.replace(bDLE + bDLE, bDLE)


class gps(object):

    def __init__(self, conn):
        self.conn = conn

    def __iter__(self):
        return self

    def read(self):

        packet = bytes()
        pkt_active = 0

        #hold last 3 bytes (initialize assuming previous byte wasn't DLE)
        #could get unlucky if start reading mid-message with 2nd data DLE (stuffed) byte as first byte seen
        #would mis-interpret as start of message, but will simply return corrupt first packet, which was invalid anyway
        b = [b'\0x00', b'\0x00', b'\0x00']
        while True:
            b[0] = self.conn.read(1)

            if len(b[0]) == 0: #timeout
                return None

            #rather than counting even/odd DLEs, look for known pattern for start/end, to prevent issues when start reading mid-message
            #end will always be <not DLE> <DLE> <ETX>
            #start will always be <not DLE> <DLE> <not DLE, not ETX> (1 byte delayed, since DLE is the start)
            if b[2][0] != DLE and b[1][0] == DLE and b[0][0] == ETX: #end of message
                if pkt_active: #only return packet if active, otherwise found end of partial message, ignore
                    packet += b[0]
                    return packet
            elif b[2][0] != DLE and b[1][0] == DLE and b[0][0] != DLE: #start of message
                pkt_active = 1
                packet += bDLE #start is delayed by 1 byte, need to put first DLE byte into packet
                packet += b[0]
            else:
                if pkt_active: #only accumulate packet data after start of message was found
                    packet += b[0]

            #shift old bytes
            b[2] = b[1]
            b[1] = b[0]


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
