# -*- coding: utf-8 -*-

"""


"""

import logging
_LOG = logging.getLogger(__name__)


import struct
import types

from tsip.constants import DLE, DLE_STRUCT, ETX, ETX_STRUCT, PI
from tsip.packets import _instantiate_report_packet	#, DATUMS


if __debug__:
    import binascii


_BYTE_STRUCT = struct.Struct('>B')


class GPS(object):
    """
    TSIP communications with a GPS.

    """

    def __init__(self, conn):
        if __debug__: _LOG.debug('GPS.__init__: conn=%s', conn)
        self.conn = conn


    def __iter__(self):
        return self


    def read_byte(self):
        b = self.conn.read(1)

        if __debug__: 
            if b:
               _LOG.debug('GPS._read_byte: b=0x%x' % (struct.unpack('>B',b)))
            else:
               _LOG.debug('GPS._read_byte: EOF')
               raise StopIteration

        return b


    def next(self):
        """
        Return the next TSIP packet.

        :returns: TSIP packet as string with leading DLE
            and trailing DLE/ETX stripped.

        This is largely based on the code found at `Brad's Duino Blog`_ although here
        the packet is just read but not parsed.

        .. Brad's Duino Blog: http://bradsduino.blogspot.com.au/2014/06/python-code-to-read-parse-tsip-data.html

        """

        packet = b''
        start = False				# Has packet started?


        while True:
            b = self.read_byte()		# raw byte 
            i = _BYTE_STRUCT.unpack(b)[0]	# integer value of byte

            if __debug__: _LOG.debug('GPS.next: i(b)=0x%x, start=%s, packet=|%s| ', i, start, binascii.hexlify(packet))

            if start is False and i == DLE:
                # Start of packet (DLE).
                #
                if __debug__: _LOG.debug('GPS.next: Start of packet')
                start = True

            elif start is True and i == ETX:
                # Possibly the end of the packet. Let's check...
                #
                if __debug__: _LOG.debug('GPS.next: start is True and i == ETX')

                try:
                    # Terminating ETX must have been preceeded by a DLE
                    # Number of DLE bytes in packet must be odd, not counting the 
                    # DLE indicating the start of the packet.
                    #
                    if _BYTE_STRUCT.unpack(packet[-1])[0] != DLE:
                        # ETX not preceeded by DLE; keep reading...
                        if __debug__: _LOG.debug('GPS.next: ETX not preceeded by DLE(%x) but by %x', DLE,  _BYTE_STRUCT.unpack(packet[-1])[0])
                        pass
                    elif (packet.count(DLE_STRUCT, 1) % 2) == 0:
                        # Number of DLE is even, not odd; keep reading...
                        if __debug__: _LOG.debug('GPS.next: Number of DLE is even')
                        pass
                    else:
                        # Passed all checks, break out of the while True loop
                        if __debug__: _LOG.debug('GPS.next: End of packet')
                        break
                except IndexError:
                    # This covers cases where `packet` is not (yet) long enough, i.e.
                    # we need to read more data.
                    pass

            elif start is False:
                # Not reading "inside" of a packet.
                #
                if __debug__: _LOG.debug('GPS.next: start is False')
                continue


            packet = packet + b
            # end while True


        # We got here because we broke out of the while True loop because all
        # ETX checks passed. 
        if __debug__: _LOG.debug('GPS.next: packet(with stuffing)=%s', binascii.hexlify(packet))


        # Remove DLE byte stuffing, i.e. sequences of DLE|DLE.
        #
        packet = packet.replace(DLE_STRUCT + DLE_STRUCT, DLE_STRUCT)
        if __debug__: _LOG.debug('GPS.next: packet(without stuffing)=%s', binascii.hexlify(packet))


        # Remove leading DLE and trailing DLE/ETX.
        #
        packet = packet[1:-1]
        if __debug__: _LOG.debug('GPS.next: packet(stripped)=%s', binascii.hexlify(packet))

        return _instantiate_report_packet(packet)
        
        


    def read(self):
        """
        `GPS.read()` is a wrapper for `GPS.next()`.

        We must deal with `GPS.next()` raising StopIteration as
        a caller of `GPS.read()` would expect such an exception.

        """

        if __debug__: _LOG.debug('GPS.read')

        try:
            return self.next()
        except StopIteration:
            raise EOFError
