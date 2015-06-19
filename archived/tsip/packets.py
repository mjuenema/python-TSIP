

import struct

from packets0x1 import *
from packets0x2 import *
from packets0x3 import *
from packets0x4 import *
from packets0x5 import *
from packets0x6 import *
from packets0x7 import *
from packets0xB import *
from packets0x8E1 import *
from packets0x8E2 import *
from packets0x8E4 import *
from packets0x8EA import *
from packets0x8F1 import *
from packets0x8F2 import *
from packets0x8F4 import *
from packets0x8FA import *

from helpers import *


class _Packet(object):
    """
    Base class for all other TSIP packet classes.

    """

    _fields = []


    def _set_value(name, value):
        try:
            i = self._names.index(name)
            self._values[i] = value
        except IndexError:
            raise AttributeError("No such attribute %s" % (name))


    def _get_value(name):
        try:
            i = self._names.index(name)
            return self._values[i]
        except IndexError:
            raise AttributeError("No such attribute %s" % (name))


    def __init__(self, pkt=None, **kwargs):

        # Split self._fields into individual lists.
        #
        (self._names, self._formats, self._values) = \
            zip(*self._fields)


        # Parse `pkt` if not ``None``.
        #
        if pkt is not None:
            try:
                self._values = struct.unpack(
                    "".join(self._formats), strip(pkt))
            except (struct.error), e:
                raise ValueError("unable to parse TSIP packet into class %s: %s" % (type(self), e)


        # Merge **kwargs into `self._field_values`.
        #
        for (name, value) in kwargs.items():
            self._set_value(name, value)


    def __getattr__(self, name):
        return self._get_value(name)


    def __setattr__(self, name, value):
        self._set_value(name, value)
