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
        # It's wrong to assume that end will always be <not DLE> <DLE> <ETX>.
        # <DLE> <DLE> <DLE> <ETX> is perfectly fine if we get one <DLE> in the end of the packet
        # for some reason, e.g. unlucky floating point number, weird product name,
        # Packet 0x45 with firmware built on year 2016, Packet 0x41 with leap second count 16,
        # Packet 0x57 with (week % 256) being 16, Packet 0x8F-AB (Primary Timing) on year 2064, etc.
        #
        # <not DLE> <DLE> <DLE> <ETX> is also a valid packet body. so we can't know if <ETX> is
        # the end of the packet or not unless we've counted true parity of <DLE> count. We can't
        # count it properly unless we've seen <not DLE>. It makes harder to skip the half-message in
        # a streaming way: series of <DLE> followed by <ETX> may be the body or end of the packet.
        #
        # [<DLE>] <ETX> <DLE> <not DLE> is always a marker of end of one packet and start of another
        # one, as non-stuffed <DLE> is only valid at the preamble.
        #
        # However, the read() usually does not see the <ETX> as the usual startup happens when the
        # wire is silent.  Waiting for <ETX> and skipping the first packet on every read() to sync
        # with the stream is suboptimal.  Storing state in the backtracking buffer is an option, but
        # re-syncing might be more robust.
        #
        # Initialize assuming previous byte wasn't DLE.  Could get unlucky if start reading
        # mid-message with 2nd data DLE (stuffed) byte as first byte seen would mis-interpret as
        # start of message, but will simply return corrupt first packet, which was invalid anyway.
        # Packet ID is never ETX or DLE, so it'll break the streak.
        streak = None
        buf = []
        while True:
            b = self.conn.read(1)
            if len(b) == 0: # timeout, EOF
                return None
            buf.append(b)
            if b == bETX and streak is not None and streak & 1:
                # That's the end of packet for sure. The head might be just fine, but it as well may
                # be polluted with the tail of the previous packet or have <DLE> <ID> chopped off.
                #  1. P endswith <non-DLE><2N+1*DLE><ETX>
                #  2. That's the only <non-DLE><2N+1*DLE><ETX> sequence in P.
                # Let's _assume_ that no bytes were skipped, e.g. by delayed calls to conn.read().
                # In this case the only possible tail of the previous packet is <N*DLE><ETX>.
                # <DLE> <ID> start does not guarantee that the frame is complete, but that's the
                # best we can hope for.  Otherwise the frame is just half-frame.
                p = b''.join(buf)
                if p[0] == DLE and p[1] not in (DLE, ETX): # common case
                    return p
                p = p.lstrip(bDLE)
                if len(p) >= 4 and p[0] == ETX and p[1] == DLE and p[2] not in (DLE, ETX):
                    return p[1:] # N=0, just <ETX>
                else:
                    buf = [] # skip half-frame, keep `streak`, TODO: decide if return None instead
            if b != bDLE:
                streak = 0
            elif streak is not None: # got <DLE> now, have seen <not DLE> before
                streak += 1

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
