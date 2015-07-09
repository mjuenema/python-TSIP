

import struct

from tsip.constants import DLE, DLE_STRUCT, ETX, ETX_STRUCT


def _extract_code_from_packet(packet):
    code = struct.unpack('>B', packet[0])[0]
    if code in [0x8f, 0x8e]:
        return struct.unpack('>H', packet[0:2])[0]
    return code

def _extract_data_from_packet(packet):
    code = _extract_code_from_packet(packet)
    if code > 255:
        return packet[2:]
    else:
        return packet[1:]


def _instantiate_report_packet(packet):
    """
    Return an instance of a Report packet class for `code`.

    """

    code = _extract_code_from_packet(packet)
    cls = _code_report_map.get(code)
    if cls is not None:
        return cls(packet)
    else:
        return None



class _Packet(object):
    _format = ''
    _values = []

    def __getitem__(self, index):
        return self._values[index]


class _Report(_Packet):

    def __init__(self, packet):
        # TODO: strip DLE, DLE+ETX if still present
        self._packet = packet

    @property
    def code(self):
        return _extract_code_from_packet(self._packet)

    
    @property
    def data(self):
        return _extract_data_from_packet(self._packet)


    @property
    def values(self):

        # TSIP superpacket?
        if self.code > 255:
            return struct.unpack(self._format, self.packet[2:])
        else:
            return struct.unpack(self._format, self.packet[1:])


class _Command(_Packet):

    def __init__(self, code, *values):
        self.code = code
        self.values = values


    def _pack_code(self):
        if self.code > 255:
            return struct.pack('>H', self.code)
        else:
            return struct.pack('>B', self.code)


    def _pack_values(self):
        return struct.pack(self._format, self._values)
        

    @property
    def packet(self):
       return _pack_code() + _pack_values()


class Error(_Report):
    """
    Parsing error

    """

    _format = '<function parse_0x13 at 0x7f4b8b8cb668>'
    _values = []


class Diagnostics(_Report):

    _format = None
    _values = None


# --- 0x1c ------------------------------------------------

class Command_1c(_Command):
    """
    Version Information.

    :param subcode: The subcode can be ``1`` (firmware version) or
        ``3`` (hardware version).

    """

    _format = '>B'
    _values = []

    def __init__(self, subcode):
        if subcode not in [1, 3]:
            raise ValueError("subcode must be either 1 or 3")

        super(Command_1c, self).__init__(0x1c, subcode)
        self._values = [subcode]


class Report_1c(_Report):
    """
    Version information.

    Report packet 0x1c is sent in reply to command packet 0x1c
    requesting version information. There are two variants of
    this packet, depending on the subcode sent in the command 
    packet. Sub-code 81 reports firmware version information,
    sub-code reports hardware version information.

    """

    _format    = None
    _format_83 = '>BIBBHBHp'
    _format_81 = '>BBBBBBBHp'
    

    def __init__(self, packet):
        super(Report0x1c, self).__super__(packet)
        if struct.unpack('>B', packet[1]) == 1:
            self._format == self._format_81
        elif struct.unpack('>B', packet[1]) == 3:
            self._format == self._format_83
        else:
            raise ValueError('sub-code of report packet 0x1c must be 1 or 3')
       

    
# ---  ------------

class Command_1e(_Command):
    """
     Clear Battery Backup, then Reset command

    """

    _format = '>B'
    _values = []


class Command_1f(_Command):
    """
     Request Software Versions command

    """

    _format = ''
    _values = []


class Command_21(_Command):
    """
     Request Current Time command

    """

    _format = ''
    _values = []


class Command_23(_Command):
    """
    Initial Position (XYZ ECEF) command

    """

    _format = '>fff'
    _values = []


class Command_24(_Command):
    """
    Request GPS Receiver Position Fix Mode command

    """

    _format = ''
    _values = []


class Command_25(_Command):
    """
    Initiate Soft Reset & Self Test command

    """

    _format = ''
    _values = []


class Command_26(_Command):
    """
    Request Health command

    """

    _format = ''
    _values = []


class Command_27(_Command):
    """
    Request Signal Levels command

    """

    _format = ''
    _values = []


class Command_2b(_Command):
    """
    Initial Position (Latitude, Longitude, Altitude)

    """

    _format = '>fff'
    _values = []


class Command_2d(_Command):
    """
    Request Oscillator Offset command

    """

    _format = ''
    _values = []


class Command_2e(_Command):
    """
    Set GPS time

    """

    _format = '>fh'
    _values = []


class Command_31(_Command):
    """
    Accurate Initial Position (XYZ ECEF) command

    """

    _format = '>fff'
    _values = []


class Command_32(_Command):
    """
    Accurate Initial Position (Latitude, Longitude, Altitude)

    """

    _format = '>fff'
    _values = []


class Command_35(_Command):
    """
    Set Request I/O Options command

    """

    _format = '>BBBB'
    _values = []


class Command_37(_Command):
    """
    Request Status and Values of Last Position and Velocity command

    """

    _format = ''
    _values = []


class Command_38(_Command):
    """
    Request/Load Satellite System Data command

    """

    _format = '>BBB'
    _values = []


class Command_3a(_Command):
    """
    Request Last Raw Measurement command

    """

    _format = '>B'
    _values = []


class Command_3c(_Command):
    """
    Request Current Satellite Tracking Status command

    """

    _format = '>B'
    _values = []


class Report_41(_Report):
    """
    GPS Time report

    """

    _format = '>fhf'
    _values = []


class Report_42(_Report):
    """
    Single-Precision Position Fix, XYZ ECEF report

    """

    _format = '>ffff'
    _values = []


class Report_43(_Report):
    """
    Velocity Fix, XYZ ECEF report

    """

    _format = '>fffff'
    _values = []


class Report_45(_Report):
    """
    Software Version Information report

    """

    _format = '>BBBBBBBBBB'
    _values = []


class Report_46(_Report):
    """
    Health of Receiver report

    """

    _format = '>BB'
    _values = []


class Report_47(_Report):
    """
    Signal Levels for all Satellites report

    """

    _format = ''
    _values = []


class Report_4a(_Report):
    """
    Single Precision LLA Position Fix report

    """

    _format = '>fffff'
    _values = []


class Report_4b(_Report):
    """
    Machine/ Code ID and Additional Status report

    """

    _format = '>BBB'
    _values = []


class Report_4d(_Report):
    """
    Oscillator Offset report

    """

    _format = '>f'
    _values = []


class Report_4e(_Report):
    """
    Response to Set GPS Time report

    """

    _format = '>c'
    _values = []


class Report_55(_Report):
    """
    None

    """

    _format = '>BBBB'
    _values = []


class Report_56(_Report):
    """
    Velocity Fix, East-North-Up (ENU) report

    """

    _format = '>fffff'
    _values = []


class Report_57(_Report):
    """
     Information About Last Computed Fix

    """

    _format = '>BBfh'
    _values = []


class Report_58(_Report):
    """
    Satellite System Data/Acknowledge from Receiver

    """

    _format = '>?????'
    _values = []


class Report_5a(_Report):
    """
    Raw Measurement Data

    """

    _format = '>BBBBBfffd'
    _values = []


class Report_5c(_Report):
    """
    Satellite Tracking Status report

    """

    _format = '>BBBBffffB'
    _values = []


class Report_69(_Report):
    """
    Receiver Acquisition Sensitivity Mode report

    """

    _format = '>B'
    _values = []


class Report_6d(_Report):
    """
    All-In-View Satellite Selection report

    """

    _format = '>Bffff'
    _values = []


class Report_82(_Report):
    """
    SBAS Correction Status report

    """

    _format = '>B'
    _values = []


class Report_83(_Report):
    """
    Double-Precision XYZ Position Fix and Bias Information report

    """

    _format = '>ddddf'
    _values = []


class Report_84(_Report):
    """
    Double-Precision LLA Position Fix and Bias Information report

    """

    _format = '>ddddf'
    _values = []


class Report_89(_Report):
    """
    Receiver Acquisition Sensitivity Mode report

    """

    _format = '>BB'
    _values = []


class Command_bb(_Command):
    """
    Set Receiver Configuration command

    """

    _format = ''
    _values = []


class Command_bc(_Command):
    """
    Set Port Configuration command

    """

    _format = ''
    _values = []


class Command_1c01(_Command):
    """
    Firmware version command

    """

    _format = ''
    _values = []


class Command_1c03(_Command):
    """
    Hardware component version command

    """

    _format = ''
    _values = []


class Report_1c81(_Report):
    """
    Firmware version report

    """

    _format = '>BBBBBBHp'
    _values = []


class Report_1c83(_Report):
    """
    Hardware component version report

    """

    _format = '>IBBHBHp'
    _values = []


class Command_8e15(_Command):
    """
    Request current Datum values command

    """

    _format = ''
    _values = []


class Command_8e26(_Command):
    """
    Write Configuration to NVS command

    """

    _format = ''
    _values = []


class Command_8e41(_Command):
    """
    Request Manufacturing Paramaters command

    """

    _format = ''
    _values = []


class Command_8e42(_Command):
    """
    Stored Production Parameters command

    """

    _format = ''
    _values = []


class Command_8e45(_Command):
    """
    Revert Configuration Segment to Default Settings and Write to NVS command

    """

    _format = '>B'
    _values = []


class Command_8e4a(_Command):
    """
    Set PPS Characteristics

    """

    _format = '>BBBdI'
    _values = []


class Command_8e4c(_Command):
    """
    Write Configuration Segment to NVS command

    """

    _format = '>B'
    _values = []


class Command_8e4e(_Command):
    """
    Set PPS output option command

    """

    _format = '>B'
    _values = []


class Command_8ea0(_Command):
    """
    Set DAC Value command

    """

    _format = '>?????'
    _values = []


class Command_8ea2(_Command):
    """
    UTC/GPS Timing command

    """

    _format = '>B'
    _values = []


class Command_8ea3(_Command):
    """
     Issue Oscillator Disciplining command

    """

    _format = '>B'
    _values = []


class Command_8ea5(_Command):
    """
    Packet Broadcast Mask command

    """

    _format = '>HH'
    _values = []


class Command_8ea6(_Command):
    """
    Self-Survey command

    """

    _format = '>B'
    _values = []


class Command_8ea8(_Command):
    """
    Request Disciplining Parameters command

    """

    _format = '>B'
    _values = []


class Command_8ea9(_Command):
    """
    Self-Survey Parameters command

    """

    _format = '>BBII'
    _values = []


class Command_8eab(_Command):
    """
    Request Primary Timing Packet command

    """

    _format = '>B'
    _values = []


class Command_8eac(_Command):
    """
    Request Supplementary Timing Packet command

    """

    _format = '>B'
    _values = []


class Report_8f15(_Report):
    """
    Current Datum Values report

    """

    _format = '>bddddd'
    _values = []


class Report_8f17(_Report):
    """
    UTM Single Precision Output report

    """

    _format = '>chfffff'
    _values = []


class Report_8f18(_Report):
    """
    UTM Double Precision Output report

    """

    _format = '>chddddf'
    _values = []


class Report_8f20(_Report):
    """
    Last Fix with Extra Information report (binary fixed point)

    """

    _format = '>BhhhHiIiBBBBBBh'
    _values = []


class Report_8f21(_Report):
    """
    Request Accuracy Information report

    """

    _format = '>BHHHHhB'
    _values = []


class Report_8f23(_Report):
    """
    Request Last Compact Fix Information report

    """

    _format = '>IHBBIIihhhH'
    _values = []


class Report_8f26(_Report):
    """
    Non-Volatile Memory Status report

    """

    _format = ''
    _values = []


class Report_8f2a(_Report):
    """
    Fix and Channel Tracking Info report (Type 1)

    """

    _format = '<function parse_0x8f2a at 0x7f4b8b832050>'
    _values = []


class Report_8f2b(_Report):
    """
    Fix and Channel Tracking Info report (Type 2)

    """

    _format = '>BBHIiIiiiiBBB'
    _values = []


class Report_8f4a(_Report):
    """
    Copernicus II GPS Receiver Cable Delay and POS Polarity

    """

    _format = '>BBBdI'
    _values = []


class Report_8f4f(_Report):
    """
    Set PPS width report

    """

    _format = ''
    _values = []


class Report_8fab(_Report):
    """
    Primary Timing Packet report

    """

    _format = '>IHhBBBBBBH'
    _values = []


class Report_8fac(_Report):
    """
    Supplemental Timing Packet

    """

    _format = '>BBBIHHBBBBffI'
    _values = []


class Report_8ea8(_Report):
    """
    Set Disciplining Parameters command (Type 0)

    """

    _format = '>ff'
    _values = []


#class Unknown_8ea801(_Unknown):
#    """
#    Set Disciplining Parameters command (Type 1)
#
#    """
#
#    _format = '>fff'
#    _values = []
#
#
#class Unknown_8ea802(_Unknown):
#    """
#    Set Disciplining Parameters command (Type 2)
#
#    """
#
#    _format = '>ff'
#    _values = []
#
#
#class Unknown_8ea803(_Unknown):
#    """
#    Set Disciplining Parameters command (Type 3)
#
#    """
#
#    _format = '>f'
#    _values = []


_code_report_map = {
        0x1e: Error,
	0x1c: Report_1c,
	0x41: Report_41,
	0x42: Report_42,
	0x43: Report_43,
	0x45: Report_45,
	0x46: Report_46,
	0x47: Report_47,
	0x4a: Report_4a,
	0x4b: Report_4b,
	0x4d: Report_4d,
	0x4e: Report_4e,
	0x56: Report_56,
	0x5c: Report_5c,
	0x5f: Diagnostics,
	0x69: Report_69,
	0x6d: Report_6d,
	0x82: Report_82,
	0x83: Report_83,
	0x84: Report_84,
	0x89: Report_89,
	0x1c81: Report_1c81,
	0x1c83: Report_1c83,
	0x8f15: Report_8f15,
	0x8f17: Report_8f17,
	0x8f18: Report_8f18,
	0x8f21: Report_8f21,
	0x8f23: Report_8f23,
	0x8f26: Report_8f26,
	0x8f4f: Report_8f4f,
	0x8fab: Report_8fab
}
"""Map the code of a TSIP report packet to the Python class."""
