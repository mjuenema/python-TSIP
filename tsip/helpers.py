
"""
Helper functions.

"""

from packets import *
from contants import *


_PACKET_TYPE_TO_CLASS_TABLE = {
    chr(0x1c): Packet0x1C,
    chr(0x1e): Packet0x1C,
    chr(0x1f): Packet0x1C,
    chr(0x24): Packet0x1C,
    chr(0x25): Packet0x1C,
    chr(0x26): Packet0x1C,
    chr(0x27): Packet0x1C,
    chr(0x29): Packet0x1C,
    chr(0x31): Packet0x1C,
    chr(0x32): Packet0x1C,
    chr(0x34): Packet0x1C,
    chr(0x35): Packet0x1C,
    chr(0x37): Packet0x1C,
    chr(0x38): Packet0x1C,
    chr(0x39): Packet0x1C,
    chr(0x3a): Packet0x1C,
    chr(0x3b): Packet0x1C,
    chr(0x3c): Packet0x1C,
    chr(0x3f): Packet0x1C,
}
"""
Mapping of TSIP packet <id> to Python classes
representing the packet.
"""


def _strip(packet):
    """
    Strip a TSIP packet of delimiters.

    TSIP packet structure is the same for both commands 
    and reports. The packet format is

        <DLE> <id> <data string bytes> <DLE> <ETX>

    The `_strip()` function removes the leading <DLE> 
    and trailing <DLE><ETX> if present.

    :param packet: TSIP packet in binary format.
    :returns: Stripped TSIP packet.
    
    Technically the return value is not a properly
    formatted TSIP packet anymore but it is somewhat 
    easier to deal without the delimiters.

    """

    return packet.rstrip(ETX).strip(DLE)


def identify(packet):
    """
    Identify the TSIP packet type.

    :param packet: TSIP packet in binary format.
    :returns: Python class representing this packet type.
    :raise ValueError: If the packet cannot be identified.

    """

    # Strip delimiters.
    #
    packet = _strip(packet)

    
    # One byte packet <id>
    #
    try:
        return _PACKET_TYPE_TO_CLASS_TABLE(packet[0])
    except KeyError:
        try:
            # Two byte packet <id> (0x8e, 0x8f)
            #
            return _PACKET_TYPE_TO_CLASS_TABLE(packet[0:2])
        except KeyError:
            raise ValueError("'%s' is not a known TSIP packet")

    
