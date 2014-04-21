
"""
All TSIP packets with identifiers starting with 0x1

"""

from constants import *
from packets import _Packet


class Packet0x13(_Packet):
    """
    Unparseable Packet report.

    """

    _fields = [("id", UINT8, chr(0x1c)]


    def __init__(self, pkt):

        # The second field in this packet contains the
        # original command packet this report packet 
        # refers to. It can be of variable length so it
        # is added on the fly here.
        #
        self._fields.append(("packet_data", "%ds" % (len(pkt)-1), None))

        # 
        #
        super(Packet0x13, self).__init__(pkt)


UnparseablePacket = Packet0x13



class Packet0x1C(_Packet):
    """
    Firmware/Hardware versions

    """
