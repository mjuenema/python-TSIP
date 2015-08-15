

from nose.tools import *

from tsip.packets import Command_1c, Report_1c


GPS_CONN = None


def setup_module():
    pass


def teardown_module():
    pass


class TestVersionInformation(object):
    """Version information"""

    @timed(2.0)
    def test_firmware_version(self):
        """Firmware version information: 0x1c(1) -> 0x1c(81)"""

        command = Command_1c(1)
        assert command.subcode == 1
        GPS_CONN.write(command)

        while True:
            report = GPS_CONN.read()

            if report.code == 0x13:
                raise ValueError('unparseable packet error')

            if report.code == 0x1c and report.subcode == 81:
                return


    @timed(2.0)
    def test_hardware_version(self):
        """Hardware version information: 0x1c(3) -> 0x1c(83)"""

        command = Command_1c(3)
        assert command.subcode == 3
        GPS_CONN.write(command)

        while True:
            report = GPS_CONN.read()

            if report.code == 0x13:
                raise ValueError('unparseable packet error')

            if report.code == 0x1c and report.subcode == 83:
                return
