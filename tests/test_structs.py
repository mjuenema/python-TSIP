from struct import Struct

from nose.tools import raises

from tsip import *


def test_endianess():
    for (key, value) in PACKET_STRUCTURES.items():
        for struct_ in value:
            try:
                assert struct_.format[0] == '>'
            except AttributeError:
                pass
            
            
def test_packetid_subcode():
    for (key, value) in PACKET_STRUCTURES.items():
        for struct_ in value:
            try:
                if key > 255:
                    assert struct_.format.startswith('>BB')
                else:
                    assert struct_.format.startswith('>B')
            except AttributeError:
                pass
            
def test_get_structs_for_rawpacket():
    for i in xrange(0, 256):
        rawpacket = chr(i)
        
        structs_ = get_structs_for_rawpacket(rawpacket)
        for struct_ in structs_:
            assert hasattr(struct_, 'pack')
            assert hasattr(struct_, 'unpack')
        
        for j in xrange(0, 256):
            rawpacket = chr(i) + chr(j)
        
            structs_ = get_structs_for_rawpacket(rawpacket)
            for struct_ in structs_:
                assert hasattr(struct_, 'pack')
                assert hasattr(struct_, 'unpack')
                
def test_get_structs_for_fields():
    for i in xrange(0, 256):
            
        structs_ = get_structs_for_fields([i])
        for struct_ in structs_:
            assert hasattr(struct_, 'pack')
            assert hasattr(struct_, 'unpack')
        
        for j in xrange(0, 256):
            structs_ = get_structs_for_fields([i, j])
            for struct_ in structs_:
                assert hasattr(struct_, 'pack')
                assert hasattr(struct_, 'unpack')