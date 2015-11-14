# -*- coding: utf-8 -*-

"""
Base classes for all TSIP packets

"""

import struct

import namedlist

#from tsip.globals import _PACKET_MAP
#from tsip.constants import DLE, DLE_STRUCT, ETX, ETX_STRUCT


class _PacketMap(object):
    _map = {}
    
    def __setitem__(self, key, value):
        self._map[key] = value
        
    def __getitem__(self, key):
        return self._map[key]
    
    def register_packet(self, code, subcode=None, cls=None):
        if subcode:
            key = struct.pack('>BB', code, subcode)
        else:
            key = struct.pack('>B', code)
            
        self[key] = cls
        
    def get_class_by_raw(self, raw):
        """Return packet class from raw TSIP data. 
        
           :raises KeyError: When no matching packet class was found.
        """
        
        try:            
            return self[raw[0:2]]
        except (KeyError, IndexError):
            return self[raw[0]]
        
        
_PACKET_MAP = _PacketMap()       


# TODO: remove this later
def _extract_code_from_raw(raw):
    code = struct.unpack('>B', raw[0])[0]
    if code in []:
        return struct.unpack('>H', raw[0:2])[0]
    return code
 
# TODO: remove this later
def register_packet(key, cls):
    """
    Register a packet with `_PACKET_MAP`
     
    :param key: The unique key for this packet. This is
 
    """
 
    global _PACKET_MAP
 
    _PACKET_MAP[key] = cls


# TODO: Move this to tsip.packet
def packet_factory(code, subcode=None, fmt=None, attrs=[], descr=None):

    class Packet(object):
        _code = None
        _subcode = None
        _fmt = None
        _attrs = []
        _descr = None
        _name = None
        
        def __init__(self, **kwargs):
#             for attr in self._attrs:
#                 self.__dict__[attr] = None
            
            for key, value in kwargs.items():
                self.__dict__[key] = value
                       
        @property
        def code(self):
            return self._code

        @property
        def subcode(self):
            return self._subcode
        
        @property
        def descr(self):
            return self._descr
        
        # TODO: pack, unpack

    

    if subcode:
        name = 'Packet_0x%02x%02x' % (code, subcode)
    else:
        name = 'Packet_0x%02x' % (code)
        
    cls = type(name, (Packet,), {})
    
    cls._code = code
    cls._subcode = subcode
    cls._fmt = fmt
    cls._attrs = attrs
    cls._descr = descr
    
   
    global _PACKET_MAP
    _PACKET_MAP.register_packet(code=code, subcode=subcode, cls=cls)


    return cls



# class _RO(object):
#     def __init__(self, i):
#         self.i = i
# 
#     def __get__(self, instance, owner):
#         return instance[self.i]
# 
# class _RW(_RO):
# 
#     def __set__(self, instance, value):
#         instance[self.i] = value


# TODO: Remove this Packet once packets1 and packets2 use the factory
class Packet(object):
    """
    Base class for `Command` and `Report` packets.

    """

    _code = None
    _subcode = None
    """Packet code and subcode."""

#    _struct = None
#    """Instance of `struct.Struct` describing the binary structure of the TSIP packet including its code."""

    _fmt = None
    """Format string for `struct.struct()` call."""

    def pack(self):
        """Generate the binary structure of the TSIP packet."""
        b = struct.pack('>B', self.code)

        if self._subcode:
            b += struct.pack('>B', self.subcode)

        if self._fmt:
            b += struct.pack(self._fmt, *self)
            # `self` works because derived classes must also derive
            # from `namedlist.namedlist`.

        # TODO: DLE padding!!!
        return b


    @property
    def code(self):
        return self._code


    @property
    def subcode(self):
        return self._subcode


class Report(Packet):
    # TODO: clean-up later
    pass

class Command(Packet):
    # TODO: clean-up later
    pass
    

