
"""
Constants related to TSIP.

"""

import struct
import datetime

DLE = 0x10
DLE_STRUCT = struct.pack('B', DLE)
"""ASCII character 16: Data Link Escape."""

ETX = 0x3
ETX_STRUCT = struct.pack('B', ETX)
"""ASCII character 3: End of Text."""

PI = 3.1415926535898
"""Pi according to Navstar GPS document (ICD-GPS-200), section 20.3.3.4.3.3
(http://www.dtic.mil/dtic/tr/fulltext/u2/a255994.pdf).

This value for Pi is slightly less accurate than the Python
version of math.pi = 3.141592653589793. The Trimble TSIP 
documentation refers to the ICD-GPS-200 value."""

GPS_EPOCH = datetime.datetime(1980, 1, 6)
"""The GPS epoch is 00:00 UTC on the first Sunday of 1980."""