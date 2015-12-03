import _tsip

command = tsip.Packet(0x1c, 0x01)
gps_conn.write(command)

while True:
    report = gps_conn.read()
    if report[0] == 0x1c and report.subcode == 0x81:
        print report
        break
# Packet(28, 129, ...)
