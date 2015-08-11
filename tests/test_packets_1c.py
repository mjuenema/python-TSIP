

from nose.tools import *

from tsip.packets1 import Command_1c, Report_1c

import helpers

def setup_module():
   helpers.setup_module()

class Test_1c(object):

    @timed(2.0)
    def test_1c_firmware_version(self):
        command = Command_1c(1)
        assert command.subcode == 1
        helpers.GPS_CONN.write(command)

        for report in GPS_CONN:
            if report.code == 0x1c:
                assert report.subcode == 0x81
                break

    @timed(2.0)
    def test_1c_hardware_version(self):
        command = Command_1c(3)
        assert command.subcode == 3
        helpers.GPS_CONN.write(command)

        for report in GPS_CONN:
            if report.code == 0x1c:
                assert report.subcode == 0x83
                break
