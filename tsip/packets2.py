

import struct

from tsip.constants import DLE, DLE_STRUCT, ETX, ETX_STRUCT


class _Report(object)

    def __init__(self, packet):
        # TODO: strip DLE, DLE+ETX if still present
        self._packet = packet

    @property
    def code(self):
        code = struct.unpack('>B', self._packet[0])

        # TSIP superpacket?
        if code in [0x8e, 0x8f]:
            return struct.unpack('>H', self._packet[0:2])
        else:
            return code

    @property
    def values(self):

        # TSIP superpacket?
        if self.code > 255:
            return struct.unpack(self._format, self.packet[2:])
        else:
            return struct.unpack(self._format, self.packet[1:])


class _Command(object):

    def __init__(self, code, *values):
        self.code = code
        self.values = values


class Error(_Report):
    """
    Parsing error

    """

    _format = '<function parse_0x13 at 0x7f4b8b8cb668>'
    _values = []


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


class Unknown_2b(_Unknown):
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


class Unknown_2e(_Unknown):
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


class Unknown_32(_Unknown):
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


class Unknown_55(_Unknown):
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


class Unknown_57(_Unknown):
    """
     Information About Last Computed Fix

    """

    _format = '>BBfh'
    _values = []


class Unknown_58(_Unknown):
    """
    Satellite System Data/Acknowledge from Receiver

    """

    _format = '>?????'
    _values = []


class Unknown_5a(_Unknown):
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


class Unknown_8e4a(_Unknown):
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


class Unknown_8f20(_Unknown):
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


class Unknown_8f2a(_Unknown):
    """
    Fix and Channel Tracking Info report (Type 1)

    """

    _format = '<function parse_0x8f2a at 0x7f4b8b832050>'
    _values = []


class Unknown_8f2b(_Unknown):
    """
    Fix and Channel Tracking Info report (Type 2)

    """

    _format = '>BBHIiIiiiiBBB'
    _values = []


class Unknown_8f4a(_Unknown):
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


class Unknown_8fac(_Unknown):
    """
    Supplemental Timing Packet

    """

    _format = '>BBBIHHBBBBffI'
    _values = []


class Unknown_8ea800(_Unknown):
    """
    Set Disciplining Parameters command (Type 0)

    """

    _format = '>ff'
    _values = []


class Unknown_8ea801(_Unknown):
    """
    Set Disciplining Parameters command (Type 1)

    """

    _format = '>fff'
    _values = []


class Unknown_8ea802(_Unknown):
    """
    Set Disciplining Parameters command (Type 2)

    """

    _format = '>ff'
    _values = []


class Unknown_8ea803(_Unknown):
    """
    Set Disciplining Parameters command (Type 3)

    """

    _format = '>f'
    _values = []

