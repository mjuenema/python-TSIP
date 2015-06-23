
"""
Constants related to TSIP.

"""

DLE = 0x10
"""ASCII character 16: Data Link Escape."""

ETX = 0x03
"""ASCII character 3: End of Text."""

PI = 3.1415926535898
"""Pi according to Navstar GPS document (ICD-GPS-200), section 20.3.3.4.3.3
(http://www.dtic.mil/dtic/tr/fulltext/u2/a255994.pdf).

This value for Pi is slightly less accurate than the Python
version of math.pi = 3.141592653589793. The Trimble TSIP 
documentation refers to the ICD-GPS-200 value."""

