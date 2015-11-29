About Python-TSIP
=================

Python-TSIP is a Python package for parsing and creating TSIP packets. The Trimble Standard 
Interface Protocol (TSIP) is the binary protocol spoken by the GPS receivers sold by Trimble Navigation Ltd. 
(http://www.trimble.com).

Status
======

Almost the full set of TSIP command and report packets understood by the Copernicus II receiver has been implemented but 
so far only some of them have been tested against the actual GPS. Implementing a complete set of tests against an actual
Copernicus II receiver is currently work in progress. Presumably Trimble Thunderbolt and Thunderbolt-E are also 
supported as they appear to implement a subset of the commands/reports of the (newer) Copernicus II receiver. 
I don't have access to any other Trimble products.

Documentation is way behind and largely reflects an obsolete implementation of this project. 

`python-TSIP` is automatically tested against the following Python versions.

* Python 2.6
* Python 2.7
* Python 3.3
* Python 3.3
* Python 3.4
* Python 3.5
* pypy
* pypy3

=========   ===================
Branch      Travis-CI          
=========   ===================
master      |travismaster|     
develop     |travisdevelop|
=========   ===================

The *master* branch equals the latest release!

.. |travismaster| image:: https://travis-ci.org/mjuenema/python-TSIP.svg?branch=master
    :target: https://travis-ci.org/mjuenema/python-TSIP
    
.. |travisdevelop| image:: https://travis-ci.org/mjuenema/python-TSIP.svg?branch=develop
    :target: https://travis-ci.org/mjuenema/python-TSIP

Example
=======

The following code shows how to receive the current GPS time from the receiver.

* Command packet 0x21 requests the current GPS time.
* Report packet 0x41 contains the current GPS time. Its fields are accessible by index.

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
       report = gps.read()
       if report.code == 0x41:
           print 'GPS time of week .......: %f' % (report[0])
           print 'Extended GPS week number: %d' % (report[1])
           print 'GPS UTC offset .........: %f' % (report[2])
           break
   
