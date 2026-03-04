import io
import itertools
import os.path

from nose.tools import *

from tsip import *


@raises(ValueError)
def test_hlgps_read_eof():
    # FIXME: that's not really a test, but a statement on weird API behavior on EOF.
    p = Packet(0x1C, 0x81, 0, 3, 2, 1, 11, 17, 2015, "productname")
    raw = frame(stuff(p.pack()))
    conn = io.BytesIO(raw + raw)
    drv = GPS(conn)
    p1 = drv.read()
    assert p1 == p
    p2 = drv.read()
    assert p2 == p
    try:
        p3 = drv.read()
    except ValueError as e:
        assert e.args == ("packet does not contain leading DLE+ID and trailing DLE/ETX",), e
        raise e


def test_llgps_read_eof():
    p = Packet(0x1C, 0x81, 0, 3, 2, 1, 11, 17, 2015, "productname")
    raw = frame(stuff(p.pack()))
    conn = io.BytesIO(raw + raw)
    drv = gps(conn)
    p1 = drv.read()
    assert p1 == raw
    p2 = drv.read()
    assert p2 == raw
    p3 = drv.read()
    assert p3 == None


def test_llgps_read_midpacket():
    for nlen in range(7):  # simple fuzzer
        for opt in itertools.product((bDLE, bETX, b"A"), repeat=nlen):
            name = b"".join(opt)
            pkt = Packet(0x1C, 0x81, 0, 3, 2, 1, 11, 17, 2015, name)
            raw = frame(stuff(pkt.pack()))

            conn = io.BytesIO(raw + raw)
            drv = gps(conn)
            assert drv.read() == drv.read() == raw

            for off in range(1, len(raw)):
                tail = raw[off:]
                conn = io.BytesIO(tail + raw)
                drv = gps(conn)
                p1 = drv.read()
                p2 = drv.read()
                p3 = drv.read()
                # Either half-packet is skipped silently && got RAW and EOF
                # OR first damaged packet looks okayish, second is RAW and EOF
                assert (p1 == raw and p2 == p3 == None) or (p1 == tail and p2 == raw and p3 is None)
