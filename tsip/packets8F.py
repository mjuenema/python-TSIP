# -*- coding: utf-8 -*-

"""
TSIP super-packet commands (0x8f??)

* 0x8f15 - Current Datum Values report.
* 0x8f17 - UTM Single Precision Output report.
* 0x8f18 - UTM Double Precision Output report.
* 0x8f20 - Last Fix with Extra Information report.
* 0x8f21 - Request Accuracy Information report.
* 0x8f23 - Request Last Compact Fix Information report.
* 0x8f26 - Non-Volatile Memory Status report.
* 0x8f2a - Fix and Channel Tracking Info report (Type 1).
* 0x8f2b - Fix and Channel Tracking Info report (Type 2).
* 0x8f4a - Copernicus II GPS Receiver Cable Delay and POS Polarity.
* 0x8f4f - Set PPS width report.
* 0x8fab - Primary Timing Packet report.
* 0x8fac - Supplemental Timing Packet.

"""

import struct
import datetime

from tsip.base import Command, Report
from tsip.misc import b0, b1, b2, b5
from tsip.constants import GPS_EPOCH



class Report_8f15(Report):
    """
    Current Datum Values report

    """

    _format = '>bddddd'
    _values = []


class Report_8f17(Report):
    """
    UTM Single Precision Output report

    """

    _format = '>chfffff'
    _values = []


class Report_8f18(Report):
    """
    UTM Double Precision Output report

    """

    _format = '>chddddf'
    _values = []


class Report_8f20(Report):
    """
    Last Fix with Extra Information report (binary fixed point)

    """

    _format = '>BhhhHiIiBBBBBBh'
    _values = []


class Report_8f21(Report):
    """
    Request Accuracy Information report

    """

    _format = '>BHHHHhB'
    _values = []


class Report_8f23(Report):
    """
    Request Last Compact Fix Information report
    
    =====   ===============================================
    Index   Description
    =====   ===============================================
    0       Fix time, GPS Time of week (ms)
    1       Week number
    2       Leap second offset (seconds)
    3       Byte 8
    4       Latitude
    5       Longitude
    6       Altitude
    7       Velocity East
    8       Velocity North
    9       Velocity Up
    10      Reserved
    =====   ===============================================

    The Velocity East, Velocity North and Velocity Up fields
    contain the raw values. In contrast, the `.velocity_east`,
    `.velocity_north` and `.velocity_up` properties contain
    the scaled values. The `.velocity_scale` property is either
    0.005 (m/s2) or 0.002 (m/s2), depending on bit 5 of Byte 8.
    
    >>> packet = gps.read()
    >>> packet
    <tsip.packets8F.Report_8f23 object at 0x14ea150>
    >>> '%x' % packet.code
    '8f23'
    >>> packet.values
    (332803000, 1851, 17, 24, -450477748, 1729905204, 59893, 0, 0, 0, 65535)
    >>> packet.fix_time
    332803000
    >>> packet.week_number
    1851
    >>> packet.leap_second_offset
    17
    >>> packet.latitude
    -33.758608646690845
    >>> packet.longitude
    142.9989791586995
    >>> packet.altitude
    59.893
    >>> packet.velocity_east
    0.0
    >>> packet.velocity_north
    0.0
    >>> packet.velocity_up
    0.0
    >>> packet.velocity_scale
    0.002
    >>> packet.fix_available
    True
    >>> packet.dgps
    False
    >>> packet.two_d
    False
    >>> packet.utc_datetime
    datetime.datetime(2015, 7, 1, 20, 26, 26)
    >>> packet.gps_datetime
    datetime.datetime(2015, 7, 1, 20, 26, 43)

    """

    _format = '>IHBBiIihhhH'
    _values = []
    
    @property
    def gps_datetime(self):
        """GPS Time of fix as `datetime` instance."""
        return GPS_EPOCH + datetime.timedelta(0,self.fix_time,0,0,0,0,self.week_number)
    
    @property
    def utc_datetime(self):
        """UTC Time of fix as `datetime` instance."""
        return GPS_EPOCH + datetime.timedelta(0,self.fix_time-self.leap_second_offset,0,0,0,0,self.week_number)
    
    @property
    def fix_time(self):
        """GPS Time of Week (ms)."""
        return self.values[0]/1000.0
    
    @property
    def week_number(self):
        """Week number."""
        return self.values[1]
    
    @property
    def leap_second_offset(self):
        """Offset between UTC and GPS time because of Leap Seconds."""
        return self.values[2]
    
    @property
    def latitude(self):
        """Latitude in -90 to +90 degrees.""" 
        return float(self.values[4]) / (2**31) * 180.0
    
    @property
    def longitude(self):
        """Longitude in 0 to 360 degrees."""
        return float(self.values[5]) / (2**31) * 180.0
    
    @property
    def altitude(self):
        """Altitude in metres."""
        return self.values[6] / 1000.0
                
    @property
    def velocity_scale(self):
        """Velocity scaling factor."""
        return 0.005 if b5(self.values[3]) else 0.002
    
    @property
    def velocity_east(self):
        """Velocity in East/West direction in m/s2."""
        return self.values[7] * self.velocity_scale
    
    @property
    def velocity_north(self):
        """Velocity in North/South direction in m/s2."""
        return self.values[8] * self.velocity_scale 
    
    @property
    def velocity_up(self):
        """Vertical velocity in m/s2."""
        return self.values[9] * self.velocity_scale
    
    @property
    def fix_available(self):
        """``True`` if a fix was available."""
        return b0(self.values[3]) == 0
    
    @property
    def dgps(self):
        """``True`` if DGPS was used."""
        return b1(self.values[3]) == 1
    
    @property
    def two_d(self):
        """``True`` if this was a 2D fix."""
        return b2(self.values[3]) == 1


class Report_8f26(Report):
    """
    Non-Volatile Memory Status report

    """

    _format = ''
    _values = []


class Report_8f2a(Report):
    """
    Fix and Channel Tracking Info report (Type 1)

    """

    _format = '<function parse_0x8f2a at 0x7f4b8b832050>'
    _values = []


class Report_8f2b(Report):
    """
    Fix and Channel Tracking Info report (Type 2)

    """

    _format = '>BBHIiIiiiiBBB'
    _values = []


class Report_8f4a(Report):
    """
    Copernicus II GPS Receiver Cable Delay and POS Polarity

    """

    _format = '>BBBdI'
    _values = []


class Report_8f4f(Report):
    """
    Set PPS width report

    """

    _format = ''
    _values = []


class Report_8fab(Report):
    """
    Primary Timing Packet report

    """

    _format = '>IHhBBBBBBH'
    _values = []


class Report_8fac(Report):
    """
    Supplemental Timing Packet

    """

    _format = '>BBBIHHBBBBffI'
    _values = []
