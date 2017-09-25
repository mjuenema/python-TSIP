from struct import Struct

from nose.tools import raises

from tsip import *


def test_endianess():
    for (key, value) in PACKET_STRUCTURES.items():
        for struct_ in value:
            try:
                assert struct_.format[0] == '>' or struct_.format[0] == 62	  # Python 2 / Python 3
            except AttributeError:
                pass


def test_packetid_subcode():
    for (key, value) in PACKET_STRUCTURES.items():
        for struct_ in value:
            try:
                if key > 255:
                    assert struct_.format[0:3] == '>BB' or struct_.format[0:3] == b'>BB'
                else:
                    assert struct_.format[0:2] == '>B' or struct_.format[0:2] == b'>B'
            except AttributeError:
                pass

# def test_get_structs_for_rawpacket():
#    for i in range(0, 256):
#        rawpacket = chr(i)
#
#        structs_ = get_structs_for_rawpacket(rawpacket)
#        for struct_ in structs_:
#            assert hasattr(struct_, 'pack')
#            assert hasattr(struct_, 'unpack')
#
#        for j in range(0, 256):
#            rawpacket = chr(i) + chr(j)
#
#            structs_ = get_structs_for_rawpacket(rawpacket)
#            for struct_ in structs_:
#                assert hasattr(struct_, 'pack')
#                assert hasattr(struct_, 'unpack')
#
# def test_get_structs_for_fields():
#    for i in range(0, 256):
#
#        structs_ = get_structs_for_fields([i])
#        for struct_ in structs_:
#            assert hasattr(struct_, 'pack')
#            assert hasattr(struct_, 'unpack')
#
#        for j in range(0, 256):
#            structs_ = get_structs_for_fields([i, j])
#            for struct_ in structs_:
#                assert hasattr(struct_, 'pack')
#                assert hasattr(struct_, 'unpack')
