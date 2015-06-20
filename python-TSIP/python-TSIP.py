# -*- coding: utf-8 -*-

"""


"""


import sys


# python-TSIP.config is the place
# for global variables.
#
import python-TSIP.config


# Setup logging and suppress a possible
# "No handlers could be found for …” warning.
# 
#
import logging
import logging.handlers
_LOG = logging.getLogger(__name__)
_LOG.addHandler(logging.NullHandler())




