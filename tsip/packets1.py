# -*- coding: utf-8 -*-

"""
TSIP packets in the 0x1? range.

* Command packet 0x1c01 - Firmware version.
* Command packet 0x1c03 - Hardware component version information.
* Report packet 0x1c81 - Firmware version.
* Report packet 0x1c83 - Hardware component version information.
* Command packet 0x1e - Clear battery backup, then reset.
* Command packet 0x1f - Request software versions.

"""

from namedlist import namedlist as nl

from tsip.base import Packet, register_packet


class Packet_0x1c01(nl('Packet_0x1c01', []),
                       Packet):
    """Command packet 0x1c - Firmware version."""
    _code = 0x1c
    _subcode = 0x01
    _format = None

register_packet(0x1c01, Packet_0x1c01)


class Packet_0x1c03(nl('Packet_0x1c03', []),
                       Packet):
    """Command packet 0x1c - Hardware component version information."""
    _code = 0x1c
    _subcode = 0x03
    _format = None

register_packet(0x1c03, Packet_0x1c03)


class Packet_0x1c81(nl('Packet_0x1c81', ['reserved1', 
                                         'major_version',
                                         'minor_version',
                                         'build_number',
                                         'month',
                                         'day',
                                         'year',
                                         'product_name']),
                       Packet):
    """Report packet 0x1c81 - Firmware version."""
    _code = 0x1c
    _subcode = 0x81
    _format = '>BBBBBBHp'

register_packet(0x1c81, Packet_0x1c81)


class Packet_0x1c83(nl('Packet_0x1c83', ['serial_number', 
                                         'build_day',
                                         'build_month',
                                         'build_year',
                                         'build_hour',
                                         'hardware_code',
                                         'hardware_id']),
                       Packet):
    """Report packet 0x1c83 - Hardware component version information."""
    _code = 0x1c
    _subcode = 0x81
    _format = '>BBIBBHBHp'

register_packet(0x1c83, Packet_0x1c83)


class Packet_0x1e(nl('Packet_0x1e', [('reset_mode', 0x4b)]),
                      Packet):
    """Command packet 0x1e - Clear battery backup, then reset."""
    _code = 0x1e
    _subcode = None
    _format = '>B'

register_packet(0x1e, Packet_0x1e)


class Packet_0x1f(nl('Packet_0x1f', []),
                  Packet):
    """Command packet 0x1f - Request software versions."""
    _code = 0x1f
    _subcode = None
    _format = None

register_packet(0x1f, Packet_0x1f)