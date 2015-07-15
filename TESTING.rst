Testing
=======

The ``tests/`` directory contains Nose_ style tests for this package.

By default the tests read from the file ``tests/packets.tsip`` which
contains output captured from a Trimble Copernicus II GPS. This can
be changed by setting the environment variable TSIPDEV to point to
a different input file or even to an actual Trimble GPS connected
to a device in the ``/dev`` filesystem. In the latter case the
environment variable ``TSIPBAUD`` can be used to change the 
baud rate from the default of 9600.

.. code-block:: console

  $ export TSIPDEV=/dev/ttyS0
  $ export TSIPBAUD=38400
  $ make test

.. _Nose: https://pypi.python.org/pypi/nose/
