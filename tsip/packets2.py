# -*- coding: utf-8 -*-

"""
TSIP packets in the 0x2? range.

* Command packet 0x21 - Request current time.
* Command packet 0x23 - Initial position (XYZ ECEF)
* Command packet 0x24 - Request GPS receiver position fix mode.
* Command packet 0x25 - Initiate soft reset & self test.
* Command packet 0x26 - Request health.
* Command packet 0x27 - Request signal levels.
* Command Packet 0x2b - Initial position (LLA).
* Command packet 0x2d - Request oscillator offset.
* Command packet 0x2e - Set GPS time.

"""

from namedlist import namedlist as nl

from tsip.base import Packet, register_packet


class Packet_0x21(nl('Packet_0x21', []),
                  Packet):
    """Command packet 0x21 - Request current time."""

    _code = 0x21
    
register_packet(0x21, Packet_0x21)
    

class Packet_0x23(nl('Packet_0x23', ['x',
                                     'y',
                                     'z',
                                     ]),
                  Packet):
    """Command packet 0x23 - Initial position (XYZ ECEF)."""
    
    _code = 0x23
    _fmt = '>fff'
    
register_packet(0x23, Packet_0x23)


class Packet_0x24(nl('Packet_0x24', []),
                  Packet):
    """Command packet 0x24 - Request GPS receiver position fix mode."""

    _code = 0x24 

register_packet(0x24, Packet_0x24)


class Packet_0x25(nl('Packet_0x25', []),
                  Packet):
    """Command packet 0x25 - Initiate soft reset & self test.""" 

    _code = 0x25
    
register_packet(0x25, Packet_0x25)


class Packet_0x26(nl('Packet_0x26', []),
                  Packet):
    """Command packet 0x26 - Request health.""" 

    _code = 0x26
    
register_packet(0x26, Packet_0x26)


class Packet_0x27(nl('Packet_0x27', []),
                  Packet):
    """Command packet 0x27 - Request signal levels.""" 

    _code = 0x27
    
register_packet(0x27, Packet_0x27)


class Packet_0x2b(nl('Packet_0x2b', ['latitude',
                                     'longitude',
                                     'altitude']),
                  Packet):
    """Command Packet 0x2b - Initial position (LLA)."""

    _code = 0x2b
    _fmt = '>fff'

register_packet(0x2b, Packet_0x2b)    


class Packet_0x2d(nl('Packet_0x2d', []),
                  Packet):
    """Command packet 0x2d - Request oscillator offset."""

    _code = 0x2d
    
register_packet(0x2d, Packet_0x2d)


class Packet_0x2e(nl('Packet_0x2e', ['gps_time_of_week',
                                     'extended_gps_week_number']),
                  Packet):
    """Command packet 0x2e - Set GPS time."""

    _code = 0x2e
    _fmt = '>fh'
    
register_packet(0x2e, Packet_0x2e)
