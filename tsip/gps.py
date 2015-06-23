# -*- coding: utf-8 -*-

"""


"""

import logging
_LOG = logging.getLogger(__name__)


import struct
import types

from tsip.constants import DLE, ETX, PI
from tsip.packets import FORMATS, DATUMS


class GPS(object):

    def __init__(self, conn):
        if __debug__: _LOG.debug('GPS.__init__: conn=%s', conn)
        self.conn = conn


    def __iter__(self):
        return self


    def read_byte(self):
        b = self.conn.read(1)

        if __debug__: 
            if b:
               _LOG.debug('GPS._read_byte: b=0x%x' % (ord(b)))
            else:
               _LOG.debug('GPS._read_byte: EOF')

        return b


    def next(self):
        """
        Return the next TSIP packet.

        :returns: TSIP packet as string with leading DLE
            and trailing DLE/ETX stripped.

        """

        packet = ''

        # Read until next DLE.
        #
        while True:
            b = self.read_byte()
            if b == '': raise StopIteration
            

            if ord(b) == DLE:
                if __debug__: _LOG.debug('GPS.next: 0x%0x == DLE (start)', ord(b))

                # Read the next byte and check whether 
                # this was a "stuffed" DLE.
                #
                b = self.read_byte()
                if b == '': raise StopIteration

                if ord(b) != DLE:
                    packet = b
                    if __debug__: _LOG.debug('GPS.next: 0x%0x not DLE (start), packet="%s"', ord(b), packet)
                    break


        # Continue reading until DLE/ETX.
        #
        while True:
           b = self.read_byte()
           if b == '': raise StopIteration

           if ord(b) <> DLE:
               packet += b
               if __debug__: _LOG.debug('GPS.next: 0x%0x not DLE (middle/end), packet="%s"', ord(b), packet)
           else:
               # ord(b) = DLE; stuffed DLE
               if __debug__: _LOG.debug('GPS.next: 0x%0x == DLE (middle/end)', ord(b))

               b = self.read_byte()
               if b == '': raise StopIteration

               if ord(b) == ETX:
                   if __debug__: _LOG.debug('GPS.next: 0x%0x == ETX (end)', ord(b))
                   break
               else:
                   packet = packet + struct.pack('>B', DLE) + b
                   if __debug__: _LOG.debug('GPS.next: 0x%0x not ETX (end), packet="%s"', ord(b), packet)


        if __debug__: _LOG.debug('GPS.next: packet="%s"' % (packet))
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

    _packet = ''
    _format = None	
    _values = None
    _args = None


    def __init__(self, id, *args):
        self.id = id
        self._args = args


        # Set self._format and initialise self._values.
        #
        self._set_format()
        self._set_values()


    def _set_format(self):
        """
        Set `self._format` by TSIP packet ID.

        """

        # Set self._format 
        #
        try:
            self._format = FORMATS[id][0]
        except KeyError:
            # The default value is simple the original 
            self._format = '>%ds' % len(self._packet)


    def _set_values(self):
        """
        Set `self._values`. 

        This method requires that `self._format` has already been set.
        If `self._args` is a list its values are copied into `self._values`.

        In the end `self._values` will be a list of values (set to defaults
        or initialised with self._args) matches `self._format` in terms
        of functions defined in Python's `struct` module.

        """

        if self._format is None:
            raise AttributeError("self._format must not be None when calling self._set_values")


        # Initialise self._values with default values unless self._format is actually
        # a custom parser/formatting function dealing with the TSIp packet.
        #
        self._values = []

        if isinstance(self._format, types.StringType):
            for f in self._format:
                if f in ['c','s','p']:
                    self._values.append('')
                if f in ['b','B','h','H','i','I','l','L','q','Q']:
                    self._values.append(0)
                elif f in ['f','d']:
                    self._values.append(0.0)
                else:
                    pass

            # Copy self._args 
            #
            if self._args is not None:
                for (i,v) in enumerate(self._args):
                    self._values[i] = v

        elif isinstance(self._format, types.FunctionType):
            if self._args is not None:
                self._values = self._args
        else:
            raise ValueError('self._format must be a string or a function')


    @classmethod
    def parse(cls, packet):
        """
        Parse a TSIP packet.

        :param packet: TSIP packet with leading DLE and trailing DLE/ETX stripped. 
        :returns: Instance of `Packet`.

        This classmethod is mainly used by the `GPS.read()` and `GPS.next()` 
        methods to return the next TSIP packet received from the GPS.

        """

        if __debug__: _LOG.debug('Packet.parse: packet=%s', packet)

        self._packet = packet
   
        # One byte ID 
        #
        self.id = struct.unpack('B',packet[0])


        # TSIP Superpackets have a tow-byte ID
        #
        if self.id in [0x8e, 0x8f]:
            self.id = struct.unpack('H',packet[0:2])


        # Set self._format and initialise self._values.
        #
        self._set_format()
        self._set_values()
       

         



#class Packet(_Packet):
#    """
#
#    :param raw: The full TSIP packet in bytes, including leading
#                DLE and trailing DLE, ETX.
#
#    """
#
#    def __init__(self, raw):
#        self.raw = bitstring.ConstBitStream(bytes=raw)
#
#        # Verify that the first byte is DLE
#        #
#        dle = self.raw.read('uintbe:8')
#        if dle != DLE: 
#            raise ValueError('Packet not starting with DLE(0x10)')
#
#        # Read the packet id. In case of TSIP superpackets
#        # the ID is two-bytes long. Packet 0x1c has a cub-code.
#        #
#        if self.raw.peek(8) in [0x8e, 0x8f, 0x1c]:
#            self.id = self.raw.read('uintbe:16')
#        else:
#            self.id = self.raw.read('uintbe:8')
#
#
#        # Find the right TSIP packet information.
#        #
#        try:
#            self._fmt, self._attrs, _doc = _PACKETS[self.id]
#        except KeyError:
#            # No packet parser available for this ID
#            self._fmt = self._attrs = _doc = None
#
#
#        # Parse the raw data into fields.
#        #
#        if self._fmt:
#            self._fields = self.raw.unpack(self._fmt)
#        else:
#            self._fields = None
#
#
#    def __getitem__(self, i):
#        return self._fields[i]
#    
#
#
#
###
