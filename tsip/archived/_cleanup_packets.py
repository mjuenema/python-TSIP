
import _packets
import pprint


PACKETS = {}


for (key, val) in _packets._PACKETS_IN.items():
    print "%x" % (key)

    assert len(val) == 3
    (f, a ,d) = val

    f_struct = ''

    if f is not None and f.find(',') > -1:
        for F in f.split(','):
            if _packets._TYPES.has_key(F):
                f_struct += _packets._TYPES[F]
            else:
                f_struct += '?'
        assert len(f_struct) == len(a)

    elif f is not None and f.find(',') == -1:
        f_struct = f
        assert len(f_struct) == len(a)

    PACKETS[key] = (f_struct, a, d)


keys = PACKETS.keys()
keys.sort()

for key in keys:

    print "    0x%x: %s" % (key, PACKETS[key])
