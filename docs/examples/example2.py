#!/usr/bin/env python

"""
More elaborate example trying to retrieve as much data as possible from a
Trimble Copernicus II GPS. It shows how to

a) Establish a connection to the GPS.
b) Send request packets to the GPS.
c) Read report packets from the GPS and extract data.

Includes code inspired and co-written by Daniel Macia.

"""

import tsip
import serial

SERIAL = '/dev/ttyAMA0'
BAUD = 38400

# Open serial connection to Copernicus II receiver
#
serial_conn = serial.Serial(SERIAL, BAUD)
gps_conn = tsip.GPS(serial_conn)


# By default the Copernicus II emits the following packets once every second
# as configured in request packet 0x35.
#
# - GPS time: 0x4a
# - Position: 0x83, 0x80, 0x8f20 (double precision)
# - Velocity: 0x43, 0x56, 0x8f20 (double precision)
# - Health of receiver: 0x46
# - Machine code/status: 0x4b 
# - Satellite information: 0x6d
# - SBAS fix mode: 0x82
#
# Set Request I/O Options
#
gps_conn.write(tsip.Packet(0x35, 0b00110011, 0b00000011, 0b00000001, 0b00101001))


# In addition this example requests the following packets. Depending on the
# type of packet this must be requested only once or repeatedly. Check the code
# below for details.
#
# Request Satellite System Data. Request each type of data once.
#
#gps_conn.write(tsip.Packet(0x38, 1, 2, 0))	# Almanac
#gps_conn.write(tsip.Packet(0x38, 1, 3, 0))	# Health
#gps_conn.write(tsip.Packet(0x38, 1, 4, 0))	# Ionosphere
#gps_conn.write(tsip.Packet(0x38, 1, 5, 0))	# UTC
#gps_conn.write(tsip.Packet(0x38, 1, 6, 0))	# Ephemeris
#
# Request Current Satellite Tracking Status of all satellites.
#
gps_conn.write(tsip.Packet(0x3c, 0))

# Request Signal Levels
#
gps_conn.write(tsip.Packet(0x27))

while True:

    # Read the next report packet.
    # NOTE: Should implement timeout here.
    #
    report = gps_conn.read()

    # Check for garbled packets. This can happen, especially at the
    # beginning when Python-TSIP tries to detect the first packet.
    # In fact the Python-TSIP library should not return such 
    # mal-formed packets in the first place. consider this a bug.
    #
    # - report id may be a string instead of the expected integer.
    # - report may be empty, i.e. an "empty" packet was read.
    #
    if len(report) == 0:
        continue
    elif isinstance(report[0], str):
        continue

   
    # Extract the report id which is in the zero'th field of the packet.
    #
    report_id = report[0]


    # Print report data
    #
    if report_id == 0xff:
        print 'Packet unknown to Python-TSIP: %s' % (['%0x' % (ord(b)) for b in report.fields[1]])

    elif report_id == 0x41:
        # GPS Time
        print 'GPS time of week: %f' % (report[1])
        print 'Extended GPS week number: %d' % (report[2])
        print 'GPS UTC offset: %f' % (report[3])

    elif report_id == 0x46:
        # Health of receiver
        print 'Status code: %d' % (report[1])
        print 'Battery backup: %s' % ('Not available' if bool(report[2] & 0b00000001) else 'OK')
        print 'Antenna feedline: %s' % ('open or short detected' if bool(report[2] & 0b00010000) else 'OK')
        print 'Type of fault: %s' % ('short detected' if bool(report[2] & 0b00100000) else 'open detected')
 
    elif report_id == 0x47:
        # Signal Levels for all Satellites
        for i in range(0, len(report[2:]), 2):
            print 'Signal level for satellite %d: %f' % (report[2+i], report[2+i+1])

        gps_conn.write(tsip.Packet(0x27))

    elif report_id == 0x4b:
        # Machine/Code ID and Additional Status
        print 'Machine ID: %d' % (report[1])
        print 'Status 1: %d' % (report[2])
        print 'Status 3: %d' % (report[3])

    elif report_id == 0x56:
        # Velocity Fix, East-North-Up (ENU)
        print 'East velocity: %f' % (report[1])
        print 'North velocity: %f' % (report[2])
        print 'Up velocity: %f' % (report[3])
        print 'Clock bias rate: %f' % (report[4])
        print 'Time of fix: %f' % (report[5])

    elif report_id == 0x55:
        # I/O options
        print 'Position: XYZ ECEF output on: %s' % (bool(report[1] & 0b00000001))
        print 'Position: LLA output on: %s' % (bool(report[1] & 0b00000010))
        print 'Position: LLA ALT output: %s' % ("MSL" if bool(report[1] & 0b00000100) else "HAE")
        print 'Position: Precision of output: %s' % ("double" if bool(report[1] & 0b00010000) else "single")
        print 'Position: Super packet output: %s' % (bool(report[1] & 0b00010000))
        print 'Velocity: XYZ ECEF output on: %s' % (bool(report[2] & 0b00000001))
        print 'Velocity: ENU output on: %s' % (bool(report[2] & 0b00000010))
        print 'Timing: Time type: %s' % ("UTC" if bool(report[3] & 0b00000001) else "GPS")
        print 'Auxiliary: Raw measurements on: %s' % (bool(report[4] & 0b00000001))
        print 'Auxiliary: Signal level unit: %s' % ("dB Hz" if bool(report[4] & 0b00001000) else "AMU")
        print 'Auxiliary: Signal levels for SV: %s' % (bool(report[4] & 0b00100000))

    elif report_id == 0x6d:
        print 'Dimension: %s' % ('3D' if report[1] & 0b00000111 == 4 else '2D')
        print 'Auto or manual: %s' % ('Manual' if bool(report[1] & 0b00001000) else 'Auto')
        print 'PDOP: %f' % (report[2])
        print 'HDOP: %f' % (report[3])
        print 'VDOP: %f' % (report[4])
        print 'TDOP: %f' % (report[5])
        print 'Satellites: %s' % (report[6:])
       
    elif report_id == 0x83:
        # Double-Precision XYZ Position Fix and Bias Information.
        print 'X coordinate: %f' % (report[1])
        print 'Y coordinate: %f' % (report[2])
        print 'Z coordinate: %f' % (report[3])
        print 'Clock bias: %f' % (report[4])
        print 'Time-of-fix: %f' % (report[5])

    elif report_id == 0x84:
        # Double-Precision LLA
        print 'Latitude (radians): %f' % (report[1])
        print 'Longitude (radians): %f' % (report[2])
        print 'Altitude: %f' % (report[3])
        print 'Clock bias rate: %f' % (report[4])
        print 'Time of fix: %f' % (report[5])
       
    elif report_id == 0x43:
        # Velocity Fix, XYZ ECEF
        print 'X velocity: %f' % (report[1])
        print 'Y velocity: %f' % (report[2])
        print 'Z velocity: %f' % (report[3])
        print 'Bias rate: %f' % (report[4])
        print 'Time-of-fix: %f' % (report[5])

    elif report_id == 0x82:
        print 'SBAS correction status: %d' % (report[1])
       
    elif report_id == 0x58:
        # Satellite System Data
        if report[1] == 1:
            if report[2] == 2:
                print "TODO: print almanac data"
                # Request almanac again?
            elif report[2] == 3:
                print "TODO: print health page"
                # Request health again?
            # and so forth... <========
     
    elif report_id == 0x5a:
        # Raw Measurement Data
        print 'Satellite PRN number: %d' % (report[1])
        print 'Pseudorange: %d' % (report[2])
        print 'Signal level: %f' % (report[3])
        print 'Code phase: %f' % (report[4])
        print 'Doppler: %f' % (report[5])
        print 'Time of measurement: %f' % (report[6])
       
    elif report_id == 0x5c:
        # Satellite tracking status
        print 'Satellite PRN number: %d' % (report[1])
        print 'Reserved: %d' % (report[2])
        print 'Channel: %d' % (report[3])
        print 'Acquisition flag: %d' % (report[4])
        print 'Ephemeris flag: %d' % (report[5])
        print 'Signal level: %f' % (report[6])
        print 'GPS time of last measurement: %f' % (report[7])
        print 'Elevation: %f' % (report[8])
        print 'Azimuth: %f' % (report[9])
        print 'Reserved: %d' % (report[10])

        gps_conn.write(tsip.Packet(0x3c, 0))
       
    elif report_id == 0x8f:
        # Super-packets
        report_subid = report[1]

        if report_subid == 0x23:
            # Last Compact Fix Information
            print 'Fix time: %d' % (report[2])
            print 'Week number: %d' % (report[3])
            print 'Leap second offset: %d' % (report[4])
            print 'Fix available bitmask: %d' % (report[5])
            print 'Latitude: %d' % (report[6])
            print 'Longitude: %d' % (report[7])
            print 'Altitude: %d' % (report[8])
            print 'East velocity: %d' % (report[9])
            print 'North velocity: %d' % (report[10])
            print 'Up velocity: %d' % (report[11])

    else:
        # Unhandled report packet.
        print 'Received unhandled report packet: %s' % (report)
