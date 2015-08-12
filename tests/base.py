
"""
Functions that are used by test modules.

"""

import os
import os.path
import stat
import logging
import signal

_LOG = logging.getLogger(__name__)

from tsip.gps import GPS
try:
    from serial import Serial
except ImportError:
    # pyserial not installed.
    pass


# -------------------------------------

# @alarm decorator - unfortunately doesn't work well 
#                    with --pdb

from nose.tools import make_decorator

class Alarm(Exception):
    pass

def sigalrm_handler(signum, frame):
    raise Alarm


def alarm(limit):
    """Test must finish within specified time limit to pass.

    This is a better @timed decorator than the one that comes
    with *nose.tools*.

    Example use::

      @alarm(1)
      def test_that_fails():
          time.sleep(2)
    """
    def decorate(func):
        def newfunc(*arg, **kw):
            signal.signal(signal.SIGALRM, sigalrm_handler)
            signal.alarm(int(limit))
            try:
                func(*arg, **kw)
            except:
                signal.alarm(0)
                raise
        newfunc = make_decorator(func)(newfunc)
        return newfunc
    return decorate

# -------------------------------------


def setup_gps():
    """
    Return an instance `tsip.gps.GPS` instance.

    Depending on the environment variables ``TSIPDEV`` and 
    ``TSIPBAUD`` the `tsip.gps.GPS` instance will read from
    a file (``TSIPDEV`` must contain the path to the file)
    or a Trimble GPS (``TSIPDEV`` must point to the serial
    device in the ``/dev`` filesystem; ``TSIPBAUD`` may set
    the baud rate, defaulting to 9600). If ``TSIPDEV`` is
    not set a default input file will be used.

    This function is called from most test modules' setup
    functions. Any exceptions will propagate to the caller.

    """

    tsipdev = os.environ.get('TSIPDEV', 'tests/copernicus2.tsip')
    tsipbaud = int(os.environ.get('TSIPBAUD', 9600))

    mode = os.stat(tsipdev).st_mode
    
    if stat.S_ISCHR(mode):
        _LOG.debug('Reading from %s at %d baud' % (tsipdev, tsipbaud))
        return GPS(Serial(tsipdev, tsipbaud))
    else:
        _LOG.debug('Reading from %s' % (tsipdev))
        return GPS(open(tsipdev, 'rb'))


    

   


