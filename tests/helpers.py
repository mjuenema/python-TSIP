
"""
Helpers for tests.

"""

TSIP_CAPTURE = 'tests/copernicus2.tsip'

import os
import tsip

GPS_CONN = None

def setup_module():
    """
    Set global `GPS_CONN`.

    """

    global GPS_CONN

    gps_dev = os.environ.get('GPS_DEV')
    gps_baud = os.environ.get('GPS_BAUD', 9600)

    if gps_dev:
        import serial

        ser_conn = serial.Serial(gps_dev, gps_baud)
        GPS_CONN = tsip.GPS(ser_conn)
    else:
        GPS_CONN = open(TSIP_CAPTURE, 'r')	# TODO: make this seek(0) at EOF.
        
        
