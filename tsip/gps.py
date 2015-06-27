# -*- coding: utf-8 -*-

"""


"""

import logging
_LOG = logging.getLogger(__name__)


import struct
import types

from tsip.constants import DLE, DLE_STRUCT, ETX, ETX_STRUCT, PI
from tsip.packets import FORMATS, DATUMS


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

        return Packet(packet)
        
        


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


class Packet(object):

    code = 0		# Dummy default
    _values = []	# List of values

    def __init__(self, arg, *values):
        """
        TSIP packet class.

        `Packet.__init__()` can be used to either parse a TSIP packet
        or create a new one. if `arg` is a string it is considered 
        a raw TSIP packet which must be parsed. If `arg` is an
        integer, it is interpreted as the TSIP packet ID.

        """

        if isinstance(arg, types.IntType):
            self.code = arg
            self._values = list(values)
        elif isinstance(arg, types.StringType):
            self.code, self._values = self._parse(arg)
        else:
            raise ValueError

        if __debug__: _LOG.debug('Packet.__init__: self.code=0x%x, self._format=%s, self._values=%s', 
                                 self.code, self._format, self._values)

    @property
    def _format(self):
        fmt = FORMATS.get(self.code)
        if __debug__: _LOG.debug("Packet._format: self.code=0x%x, format=%s", self.code, fmt)

        return fmt


    def __getitem__(self, i):
        """
        Access fields of this TSIP packet by index.

        """

        return self._values[i]


    def __len__(self):
        """
        Return the number of fields this TSIP packet contains
        as implemented in this class.

        """

        if isinstance(self._format, types.StringType):
            return len(filter(lambda c: c in ['c','b','B','h','H','i','I','l','L','q','Q','f','d','s','p','P'], self._format))
        elif isinstance(self._format, types.FunctionType):
            # Not yet implemented
            return -1
        elif isinstance(self._format, types.NoneType):
            return 0
        else:
            # Shouldn't really get here!
            raise AttributeError("type(self._format)=%s, neither string nor function", type(self._format))



    def _parse(self, packet):
        """
        Parse a TSIP packet.

        :param packet: TSIP packet with leading DLE and trailing DLE/ETX stripped. 
        :returns: Tuple of (code, [values, ...]).

        """

        if __debug__: _LOG.debug('Packet._parse: packet=%s', binascii.hexlify(packet))

   
        # One byte ID 
        #
        code = struct.unpack('B',packet[0])[0]
        codelen = 1


        # TSIP Superpackets have a two-byte ID
        #
        if code in [0x8e, 0x8f]:
            code = struct.unpack('H',packet[0:2])[0]
            codelen = 2


        # Even though we return the Packet code we must set it here already
        # so that the `Packet._format` property can work already,
        #
        self.code = code


        # Unpack the values
        #
        if __debug__: _LOG.debug("Packet._parse: type(self._format=%s", type(self._format))

        if isinstance(self._format, types.StringType):
            values = struct.unpack(self._format, packet[codelen:])
        elif isinstance(self._format, types.FunctionType) or isinstance(self._format, types.LambdaType):
            values = self._format(packet[len(code):])
        else:
            values = []

        if __debug__: _LOG.debug('Packet._parse: code=0x%x, values=%s', code, values)

        return (code, values)


    def format_code(self):
        if self.code <= 255:
            return struct.pack('>B', self.code)
        elif 256 <= self.code <= 65335:
            return struct.pack('>H', self.code)
        else:
            raise ValueError


    def format(self):
        if isinstance(self._format, types.StringType):
            packed = self.format_code() + struct.pack(self._format, *self._values)
        elif isinstance(self._format, types.FunctionType) or isinstance(self._format, types.LambdaType):
            packed = self.format_code() + self._format(*self._values)

        # TODO: DLE stuffing
        return packed


    def __repr__(self):
        return "Packet(0x%x, %s)" % (self.code, self._values)

    

