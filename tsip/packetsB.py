# -*- coding: utf-8 -*-

"""
TSIP packets in the 0xb? range.

* 0xbb - Set Receiver Configuration command.
* 0xbc - Set Port Configuration command.

"""


import struct

from tsip.base import _Command, _Report


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
