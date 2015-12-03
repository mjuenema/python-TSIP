|pypiversions| |pypistatus| |pythontsiplicense|
 
.. |pypiversions| image:: https://img.shields.io/pypi/pyversions/python-TSIP.svg

.. |pypistatus| image::  https://img.shields.io/pypi/status/python-TSIP.svg

.. |pythontsiplicense| image:: https://img.shields.io/github/license/mjuenema/python-TSIP.svg

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

Documentation is way behind and largely reflects an obsolete implementation of this project. 

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

====================   ===================   ==============   =================
Branch                 Travis-CI             Codacy           Codecov
====================   ===================   ==============   =================
master                 |travismaster|        |codacymaster|   |codecovmaster|
develop                |travisdevelop|                        |codecovdevelop|
====================   ===================   ==============   =================

The master_ branch equals the latest release. The develop_ branch represents the latest development but may not always pass all tests. I use the gitflow_ plugin to follow this `Git branching model`_.

.. _master: https://github.com/mjuenema/python-TSIP/tree/master

.. _develop: https://github.com/mjuenema/python-TSIP/tree/develop

.. _gitflow: https://github.com/nvie/gitflow

.. _`Git branching model`: http://nvie.com/posts/a-successful-git-branching-model/

.. |travismaster| image:: https://travis-ci.org/mjuenema/python-TSIP.svg?branch=master
    :target: https://travis-ci.org/mjuenema/python-TSIP
    
.. |travisdevelop| image:: https://travis-ci.org/mjuenema/python-TSIP.svg?branch=develop
    :target: https://travis-ci.org/mjuenema/python-TSIP
    
.. |codacymaster| image:: https://api.codacy.com/project/badge/grade/91b7ca0231a24e3288ac88ff5085af42
    :target: https://www.codacy.com/app/markus_2/python-TSIP
    
.. |codecovmaster| image:: https://codecov.io/github/mjuenema/python-TSIP/coverage.svg?branch=master
    :target: https://codecov.io/github/mjuenema/python-TSIP?branch=master
    
.. |codecovdevelop| image:: https://codecov.io/github/mjuenema/python-TSIP/coverage.svg?branch=develop
    :target: https://codecov.io/github/mjuenema/python-TSIP?branch=develop
    
.. |githubtag| image:: https://img.shields.io/github/tag/mjuenema/docker-eclipse-pydev.svg

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
       if report[0] == 0x41:
           print 'GPS time of week .......: %f' % (report[1])
           print 'Extended GPS week number: %d' % (report[2])
           print 'GPS UTC offset .........: %f' % (report[3])
           break
   
