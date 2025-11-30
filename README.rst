.. image:: https://img.shields.io/pypi/v/tsip.svg?style=flat-square
   :target: https://pypi.python.org/pypi/tsip
   :alt: Version

.. image:: https://img.shields.io/github/license/mjuenema/python-TSIP.svg?style=flat-square
   :target: https://opensource.org/licenses/BSD-2-Clause
   :alt: License

.. image:: https://img.shields.io/github/issues/mjuenema/python-TSIP.svg?style=flat-square
   :target: https://github.com/mjuenema/python-TSIP/issues
   :alt: Issues

.. image:: https://img.shields.io/travis/mjuenema/python-TSIP/master.svg?style=flat-square
   :target: https://www.travis-ci.org/mjuenema/python-TSIP/builds
   :alt: Travis-CI


About Python-TSIP
=================

Python-TSIP is a Python package for parsing and creating TSIP packets. The Trimble Standard 
Interface Protocol (TSIP) is the binary protocol spoken by the GPS receivers sold by Trimble Navigation Ltd. 
(http://www.trimble.com).

Python-TSIP is available under the "BSD 2-Clause Simplified License".

Status
======

Almost the full set of TSIP command and report packets understood by the Copernicus II receiver has been implemented but 
so far only some of them have been tested against the actual GPS. Implementing a complete set of tests against an actual
Copernicus II receiver is currently work in progress. Presumably Trimble Thunderbolt and Thunderbolt-E are also 
supported as they appear to implement a subset of the commands/reports of the (newer) Copernicus II receiver. 
I don't have access to any other Trimble products.

Python-TSIP is automatically tested against the following Python versions.

* Python 2.6
* Python 2.7
* Python 3.3
* Python 3.4
* Python 3.5
* pypy
* pypy3

The tests currently fail on the following Python versions. 

* Python 3.2 (syntax error in the coverage module, it may work otherwise)
* Jython (can't get Tox to work with jython)

The master branch equals the latest release. The develop branch represents the
latest development but may not always pass all tests.


Example
=======

The following code shows how to receive the current GPS time from the receiver.

* Command packet 0x21 requests the current GPS time.
* Report packet 0x41 contains the current GPS time. Its fields are accessible by index.

Simple example for Python 3:

.. code-block:: python

   import tsip
   import serial

   # Open serial connection to Trimble receiver
   serial_conn = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
   gps_conn = tsip.GPS(serial_conn)

   # Prepare and send command packet 0x21
   gps_conn.write(tsip.Packet(0x21))

   while True:
       try:
           report = gps_conn.read()
           if report[0] == 0x41: #got response to 0x21
               print(f"GPS time of week .......: {report[1]}")
               print(f"Extended GPS week number: {report[2]}")
               print(f"GPS UTC offset .........: {report[3]}")
               break
           else: #some other packet received, output packet number
               print(f"Received packet: {hex(report[0])}")
       except ValueError:
           pass #ignore failed reads

Based on original Python 2 example:

.. code-block:: python

   import tsip
   import serial

   # Open serial connection to Copernicus II receiver
   serial_conn = serial.Serial('/dev/ttyS0', 38400)
   gps_conn = tsip.GPS(serial_conn)

   # Prepare and send command packet 0x21
   command = tsip.Packet(0x21)
   gps_conn.write(command)

   while True:      # should implement timeout here!!!
       report = gps_conn.read()
       if report[0] == 0x41:
           print 'GPS time of week .......: %f' % (report[1])
           print 'Extended GPS week number: %d' % (report[2])
           print 'GPS UTC offset .........: %f' % (report[3])
           break

More examples can be found in the `docs/examples/` folder (haven't been updated to work with Python 3)
