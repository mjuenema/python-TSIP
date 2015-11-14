# -*- coding: utf-8 -*-

"""
TSIP packets in the 0xb? range.

* 0xbb - Set Receiver Configuration command.
* 0xbc - Set Port Configuration command.

"""


import struct

from tsip.base import Command, Report


class Command_bb(Command):
    """
    Set Receiver Configuration command

    """

    _fmt = ''
    _values = []


class Command_bc(Command):
    """
    Set Port Configuration command

    """

    _fmt = ''
    _values = []
