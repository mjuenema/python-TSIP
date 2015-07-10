#!/bin/env python

import _packets
import packets

keys = _packets._PACKETS_IN.keys()
keys.sort()

for key in keys:
    try:
        fmt = packets.FORMATS[key]
    except KeyError:
        fmt = '>?????'

    doc = _packets._PACKETS_IN[key][2]


    try:
        if doc.endswith('command'):
            name = 'Command'
        elif doc.endswith('report'):
            name = 'Report'
        else:
            name = 'Unknown'
    except AttributeError:
        name = 'Unknown'

    

    print '''
class %s_%x(_%s):
    """
    %s

    """

    _format = '%s'
    _values = []
''' % (name, key, name, doc, fmt)

#    if name == 'Command':
#        print '''
#        def __init__(self, *args):
#
#            self._values = args
#
#        '''
#
#    elif name == 'Report':
#        print '''
#        def __init__(self, packet):
#
#            self._packet = packet
#
#        '''


