*********
Reference
*********

`python-TSIP` provides high-level and low-level APIs for communicating with 
Trimble GPS receivers. Both API are available by importing the `tsip` module.

The high-level API provides two classes, 
`tsip.Packet` for encoding and decoding TSIP packets, and
`tsip.GPS`, for sending these packets to a GPS and receving packets from the GPS.

The low-level API provides one class, `tsip.gps` (lower-case, in violation of PEP-8!)
for communicating with a GPS and functions for encoding and decoding TSIP packets as 
binary strings. 

In most cases a developer will only use the two classes of the high-level API.

.. important:: Neither API is fully stable yet. I am currently contemplating 
               removing the `Packet.code` and `Packet.subcode` attributes and
               making them accessible as `Packet[0]` and `Packet[1]` (if
               applicable) instead. The actual packet data fields would then
               be shifted accordingly, e.g. `Packet[2]`, `Packet[3]`, etc. This
               would make the implementation much cleaner.


High-level API
==============

Communicating with a GPS (`tsip.GPS` class)
-------------------------------------------

The high-level API provides the `tsip.GPS()` class for sending `tsip.Packet()` commands
to a Trimble GPS and reading `tsip.Packet()` reports from the GPS.

.. code-block:: python

   >>> import tsip
   >>> import serial    # pySerial (https://pypi.python.org/pypi/pyserial)
   >>> serial_conn = serial.Serial('/dev/ttyS0', 9600)
   >>> gps_conn = tsip.GPS(serial_conn)
   >>> command = Packet(0x21)
   >>> gps_conn.write(command)
   >>> while True:      # should implement timeout here!!!
   ...     report = gps_conn.read()
   ...         if report.code == 0x41:
   ...             print 'GPS time of week .......: %f' % (report[0])
   ...             print 'Extended GPS week number: %d' % (report[1])
   ...             print 'GPS UTC offset .........: %f' % (report[2])
   ...             break

Instances of `tsip.GPS` can also be iterated over.

.. code-block:: python

   >>> for packet in gps_conn:
   ...     print packet.code


TSIP Packets (`tsip.Packet` class)
----------------------------------

Not all Trimble GPS receivers support all TSIP packets.
Check the official documentation for more details and additional information.

Command Packets
~~~~~~~~~~~~~~~
 
0x1C - Firmware Version 01
..........................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x1c", ""
   "packet.subcode", "0x01", "" 


.. code-block:: python

   >>> command = Packet(0x1c, 0x01)
   >>> command.code     # 0x1c
   28
   >>> command.subcode  # 0x01
   1
   >>> gps_conn.write(command)
   >>> while True:
   ...     report = gps_conn.read()
   ...     if report.code == 0x1c and report.subcode == 0x81:
   ...         print report
   ...         break
   Packet(0x1c, 0x81
   

0x1C - Firmware Version 03
..........................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x1c", ""
   "packet.subcode", "0x03", "" 


.. code-block:: python

   >>> command = Packet(0x1c, 0x03)
   >>> command.code     # 0x1c
   28
   >>> command.subcode  # 0x03
   3
   >>> gps_conn.write(command)
   >>> while True:
   ...     report = gps_conn.read()
   ...     if report.code == 0x1c and report.subcode == 0x83:
   ...         print report
   ...         break
   Packet(0x1c, 0x83

 
0x1E - Clear Battery Backup, then Reset
.......................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x1e", ""
   "packet.subcode", "None", "" 
   "packet[0]", "Reset type", ""


.. code-block:: python

   >>> command = Packet(0x1e, 0x46)    # 0x46 = factory reset
   >>> command.code     # 0x1e
   30
   >>> command.subcode  # None
   None
   >>> gps_conn.write(command)

 
0x1F - Request Software Versions
................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x1f", ""
   "packet.subcode", "None", "" 


.. code-block:: python

   >>> packet = Packet(0x1f)
   >>> packet.code     # 0x1f
   31
   >>> packet.subcode  # None
   None
   >>> gps_conn.write(command)
   >>> while True:
   ...     report = gps_conn.read()
   ...     if report.code == 0x45:
   ...         print report
   ...         break
   Packet(0x45

 
0x21 - Request Current Time
...........................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x21", ""
   "packet.subcode", "None", "" 


.. code-block:: python

   >>> packet = Packet(0x21)
   >>> packet.code     # 0x21
   33
   >>> packet.subcode  # None
   None


 
0x23 - Initial Position (XYZ ECEF)
..................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x23", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""
   "packet[1]", "DESC", ""
   "packet[2]", "DESC", ""


.. code-block:: python

   >>> packet = Packet(0x23, 1.0, 1.0, 1.0)
   >>> packet.code     # 0x23
   35
   >>> packet.subcode  # None
   None

 
0x24 - Request GPS Receiver Position Fix Mode
.............................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x24", ""
   "packet.subcode", "None", "" 


.. code-block:: python

   >>> command = Packet(0x24)
   >>> command.code     # 0x24
   36
   >>> command.subcode  # None
   None
   >>> gps_conn.write(command)
   >>> while True:
   ...     report = gps_conn.read()
   ...     if report.code == 0x6d:
   ...         print report
   ...         break
   Packet(0x6d

 
0x25 - Initiate Soft Reset & Self Test
......................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x25", ""
   "packet.subcode", "None", "" 


.. code-block:: python

   >>> command = Packet(0x25)
   >>> command.code     # 0x25
   37
   >>> command.subcode  # None
   None
   >>> gps_conn.write(command)

 
0x26 - Request Health
.....................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x26", ""
   "packet.subcode", "None", "" 


.. code-block:: python

   >>> command = Packet(0x26)
   >>> command.code     # 0x26
   38
   >>> command.subcode  # None
   None
   >>> gps_conn.write(command)
   >>> while True:
   ...     report = gps_conn.read()
   ...     if report.code == 0x46 or report.code == 0x4b:
   ...         print report
   ...         break
   Packet(0x4b


 
0x27 - Request Signal Levels
............................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x27", ""
   "packet.subcode", "None", "" 


.. code-block:: python

   >>> command = Packet(0x27)
   >>> command.code     # 0x27
   39
   >>> command.subcode  # None
   None
   >>> gps_conn.write(command)
   >>> while True:
   ...     report = gps_conn.read()
   ...     if report.code == 0x47:
   ...         print report
   ...         break
   Packet(0x47


 
0x2B - Initial Position (Latitude, Longitude, Altitude)
.......................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x2b", ""
   "packet.subcode", "None", "" 


.. code-block:: python

   >>> packet = Packet(0x2b)
   >>> packet.code     # 0x2b
   43
   >>> packet.subcode  # None
   None


 
0x2D - Request Oscillator Offset
................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x2d", ""
   "packet.subcode", "None", "" 


.. code-block:: python

   >>> packet = Packet(0x2d)
   >>> packet.code     # 0x2d
   45
   >>> packet.subcode  # None
   None


 
0x2E - Set GPS Time
...................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x2e", ""
   "packet.subcode", "None", "" 


.. code-block:: python

   >>> packet = Packet(0x2e)
   >>> packet.code     # 0x2e
   46
   >>> packet.subcode  # None
   None


 
0x31 - Accurate Initial Position (XYZ ECEF)
...........................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x31", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""
   "packet[1]", "DESC", ""
   "packet[2]", "DESC", ""


.. code-block:: python

   >>> packet = Packet(0x31, 1.0, 1.0, 1.0)
   >>> packet.code     # 0x31
   49
   >>> packet.subcode  # None
   None


 
0x32 - Accurate Initial Position, (Latitude, Longitude, Altitude)
.................................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x32", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""
   "packet[1]", "DESC", ""
   "packet[2]", "DESC", ""


.. code-block:: python

   >>> packet = Packet(0x32, 1.0, 1.0, 1.0)
   >>> packet.code     # 0x32
   50
   >>> packet.subcode  # None
   None


 
0x35 - Set Request I/O Options
..............................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x35", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""
   "packet[1]", "DESC", ""
   "packet[2]", "DESC", ""
   "packet[3]", "DESC", ""


.. code-block:: python

   >>> packet = Packet(0x35, 100, 100, 100, 100)
   >>> packet.code     # 0x35
   53
   >>> packet.subcode  # None
   None


 
0x37 - Request Status and Values of Last Position and Velocity
..............................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x37", ""
   "packet.subcode", "None", "" 


.. code-block:: python

   >>> packet = Packet(0x37)
   >>> packet.code     # 0x37
   55
   >>> packet.subcode  # None
   None


 
0x38 - Request/Load Satellite System Data
.........................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x38", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""
   "packet[1]", "DESC", ""
   "packet[2]", "DESC", ""


.. code-block:: python

   >>> packet = Packet(0x38, 100, 100, 100)
   >>> packet.code     # 0x38
   56
   >>> packet.subcode  # None
   None


 
0x3A - Request Last Raw Measurement
...................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x3a", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""


.. code-block:: python

   >>> packet = Packet(0x3a, 100)
   >>> packet.code     # 0x3a
   58
   >>> packet.subcode  # None
   None


 
0x3C - Request Current Satellite Tracking Status
................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x3c", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""


.. code-block:: python

   >>> packet = Packet(0x3c, 100)
   >>> packet.code     # 0x3c
   60
   >>> packet.subcode  # None
   None


 
0x69 - Receiver Acquisition Sensitivity Mode
............................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x69", ""
   "packet.subcode", "None", "" 


.. code-block:: python

   >>> packet = Packet(0x69)
   >>> packet.code     # 0x69
   105
   >>> packet.subcode  # None
   None


 
0x7E - TAIP Message Output
..........................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x7e", ""
   "packet.subcode", "None", "" 


.. code-block:: python

   >>> packet = Packet(0x7e)
   >>> packet.code     # 0x7e
   126
   >>> packet.subcode  # None
   None


 
0x8E-17 - Request Last Position or Auto-Report Position in UTM Single Precision Format
......................................................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x8e", ""
   "packet.subcode", "0x17", "" 


.. code-block:: python

   >>> packet = Packet(0x8e, 0x17)
   >>> packet.code     # 0x8e
   142
   >>> packet.subcode  # 0x17
   23


 
0x8E-20 - Request Last Fix with Extra Information
.................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x8e", ""
   "packet.subcode", "0x20", "" 


.. code-block:: python

   >>> packet = Packet(0x8e, 0x20)
   >>> packet.code     # 0x8e
   142
   >>> packet.subcode  # 0x20
   32


 
0x8E-21 - Request Accuracy Information
......................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x8e", ""
   "packet.subcode", "0x21", "" 


.. code-block:: python

   >>> packet = Packet(0x8e, 0x21)
   >>> packet.code     # 0x8e
   142
   >>> packet.subcode  # 0x21
   33


 
0x8E-23 - Request Last Compact Fix Information
..............................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x8e", ""
   "packet.subcode", "0x23", "" 
   "packet[0]", "DESC", ""


.. code-block:: python

   >>> packet = Packet(0x8e, 0x23, 100)
   >>> packet.code     # 0x8e
   142
   >>> packet.subcode  # 0x23
   35


 
0x8E-26 - Non-Volatile Memory Storage
.....................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x8e", ""
   "packet.subcode", "0x26", "" 


.. code-block:: python

   >>> packet = Packet(0x8e, 0x26)
   >>> packet.code     # 0x8e
   142
   >>> packet.subcode  # 0x26
   38


 
0x8E-2A - Request Fix and Channel Tracking Info, Type 1
.......................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x8e", ""
   "packet.subcode", "0x2a", "" 


.. code-block:: python

   >>> packet = Packet(0x8e, 0x2a)
   >>> packet.code     # 0x8e
   142
   >>> packet.subcode  # 0x2a
   42


 
0x8E-2B - Request Fix and Channel Tracking Info, Type 2
.......................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x8e", ""
   "packet.subcode", "0x2b", "" 


.. code-block:: python

   >>> packet = Packet(0x8e, 0x2b)
   >>> packet.code     # 0x8e
   142
   >>> packet.subcode  # 0x2b
   43


 
0x8E-4F - Set PPS Width
.......................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x8e", ""
   "packet.subcode", "0x4f", "" 


.. code-block:: python

   >>> packet = Packet(0x8e, 0x4f)
   >>> packet.code     # 0x8e
   142
   >>> packet.subcode  # 0x4f
   79


 
0xBB - Navigation Configuration
...............................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0xbb", ""
   "packet.subcode", "None", "" 


.. code-block:: python

   >>> packet = Packet(0xbb)
   >>> packet.code     # 0xbb
   187
   >>> packet.subcode  # None
   None


 
0xBC - Protocol Configuration
.............................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0xbc", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""


.. code-block:: python

   >>> packet = Packet(0xbc, 100)
   >>> packet.code     # 0xbc
   188
   >>> packet.subcode  # None
   None


 
0xC0 - Graceful Shutdown and Go To Standby Mode
...............................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0xc0", ""
   "packet.subcode", "None", "" 


.. code-block:: python

   >>> packet = Packet(0xc0)
   >>> packet.code     # 0xc0
   192
   >>> packet.subcode  # None
   None


 
0xC2 - SBAS SV Mask.
....................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0xc2", ""
   "packet.subcode", "None", "" 


.. code-block:: python

   >>> packet = Packet(0xc2)
   >>> packet.code     # 0xc2
   194
   >>> packet.subcode  # None
   None

Report Packets
~~~~~~~~~~~~~~
 
0x41 - GPS Time
...............

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x41", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""
   "packet[1]", "DESC", ""
   "packet[2]", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x41:
   ...     packet.subcode      # None 
   None
   ...     packet[0]	#
   1.0
   ...     packet[1]	#
   100
   ...     packet[2]	#
   1.0
 
0x42 - Single-Precision Position Fix, XYZ ECEF
..............................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x42", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""
   "packet[1]", "DESC", ""
   "packet[2]", "DESC", ""
   "packet[3]", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x42:
   ...     packet.subcode      # None 
   None
   ...     packet[0]	#
   1.0
   ...     packet[1]	#
   1.0
   ...     packet[2]	#
   1.0
   ...     packet[3]	#
   1.0
 
0x43 - Velocity Fix, XYZ ECEF
.............................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x43", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""
   "packet[1]", "DESC", ""
   "packet[2]", "DESC", ""
   "packet[3]", "DESC", ""
   "packet[4]", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x43:
   ...     packet.subcode      # None 
   None
   ...     packet[0]	#
   1.0
   ...     packet[1]	#
   1.0
   ...     packet[2]	#
   1.0
   ...     packet[3]	#
   1.0
   ...     packet[4]	#
   1.0
 
0x45 - Software Version Information
...................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x45", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""
   "packet[1]", "DESC", ""
   "packet[2]", "DESC", ""
   "packet[3]", "DESC", ""
   "packet[4]", "DESC", ""
   "packet[5]", "DESC", ""
   "packet[6]", "DESC", ""
   "packet[7]", "DESC", ""
   "packet[8]", "DESC", ""
   "packet[9]", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x45:
   ...     packet.subcode      # None 
   None
   ...     packet[0]	#
   100
   ...     packet[1]	#
   100
   ...     packet[2]	#
   100
   ...     packet[3]	#
   100
   ...     packet[4]	#
   100
   ...     packet[5]	#
   100
   ...     packet[6]	#
   100
   ...     packet[7]	#
   100
   ...     packet[8]	#
   100
   ...     packet[9]	#
   100
 
0x46 - Health of Receiver
.........................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x46", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""
   "packet[1]", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x46:
   ...     packet.subcode      # None 
   None
   ...     packet[0]	#
   100
   ...     packet[1]	#
   100
 
0x47 - Signal Levels for all Satellites
.......................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x47", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""
   "packet[1]", "DESC", ""
   "packet[2]", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x47:
   ...     packet.subcode      # None 
   None
   ...     packet[0]	#
   100
   ...     packet[1]	#
   100
   ...     packet[2]	#
   1.0
 
0x4A - Single Precision LLA Position Fix
........................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x4a", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""
   "packet[1]", "DESC", ""
   "packet[2]", "DESC", ""
   "packet[3]", "DESC", ""
   "packet[4]", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x4a:
   ...     packet.subcode      # None 
   None
   ...     packet[0]	#
   1.0
   ...     packet[1]	#
   1.0
   ...     packet[2]	#
   1.0
   ...     packet[3]	#
   1.0
   ...     packet[4]	#
   1.0
 
0x4B - Machine/Code ID and Additional Status
............................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x4b", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""
   "packet[1]", "DESC", ""
   "packet[2]", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x4b:
   ...     packet.subcode      # None 
   None
   ...     packet[0]	#
   100
   ...     packet[1]	#
   100
   ...     packet[2]	#
   100
 
0x4D - Oscillator Offset
........................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x4d", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x4d:
   ...     packet.subcode      # None 
   None
   ...     packet[0]	#
   1.0
 
0x4E - Response to Set GPS Time
...............................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x4e", ""
   "packet.subcode", "None", "" 


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x4e:
   ...     packet.subcode      # None 
   None
 
0x55 - I/O Options
..................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x55", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""
   "packet[1]", "DESC", ""
   "packet[2]", "DESC", ""
   "packet[3]", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x55:
   ...     packet.subcode      # None 
   None
   ...     packet[0]	#
   100
   ...     packet[1]	#
   100
   ...     packet[2]	#
   100
   ...     packet[3]	#
   100
 
0x56 - Velocity Fix, East-North-Up (ENU)
........................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x56", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""
   "packet[1]", "DESC", ""
   "packet[2]", "DESC", ""
   "packet[3]", "DESC", ""
   "packet[4]", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x56:
   ...     packet.subcode      # None 
   None
   ...     packet[0]	#
   1.0
   ...     packet[1]	#
   1.0
   ...     packet[2]	#
   1.0
   ...     packet[3]	#
   1.0
   ...     packet[4]	#
   1.0
 
0x57 - Information About Last Computed Fix
..........................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x57", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""
   "packet[1]", "DESC", ""
   "packet[2]", "DESC", ""
   "packet[3]", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x57:
   ...     packet.subcode      # None 
   None
   ...     packet[0]	#
   100
   ...     packet[1]	#
   100
   ...     packet[2]	#
   1.0
   ...     packet[3]	#
   100
 
0x58 - Satellite System Data/Acknowledge from Receiver
......................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x58", ""
   "packet.subcode", "None", "" 


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x58:
   ...     packet.subcode      # None 
   None
 
0x5A - Raw Measurement Data
...........................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x5a", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""
   "packet[1]", "DESC", ""
   "packet[2]", "DESC", ""
   "packet[3]", "DESC", ""
   "packet[4]", "DESC", ""
   "packet[5]", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x5a:
   ...     packet.subcode      # None 
   None
   ...     packet[0]	#
   100
   ...     packet[1]	#
   1.0
   ...     packet[2]	#
   1.0
   ...     packet[3]	#
   1.0
   ...     packet[4]	#
   1.0
   ...     packet[5]	#
   1.0
 
0x5C - Satellite Tracking Status
................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x5c", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""
   "packet[1]", "DESC", ""
   "packet[2]", "DESC", ""
   "packet[3]", "DESC", ""
   "packet[4]", "DESC", ""
   "packet[5]", "DESC", ""
   "packet[6]", "DESC", ""
   "packet[7]", "DESC", ""
   "packet[8]", "DESC", ""
   "packet[9]", "DESC", ""
   "packet[10]", "DESC", ""
   "packet[11]", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x5c:
   ...     packet.subcode      # None 
   None
   ...     packet[0]	#
   100
   ...     packet[1]	#
   100
   ...     packet[2]	#
   100
   ...     packet[3]	#
   100
   ...     packet[4]	#
   1.0
   ...     packet[5]	#
   1.0
   ...     packet[6]	#
   1.0
   ...     packet[7]	#
   1.0
   ...     packet[8]	#
   100
   ...     packet[9]	#
   100
   ...     packet[10]	#
   100
   ...     packet[11]	#
   100
 
0x5F - Diagnostic Use Only
..........................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x5f", ""
   "packet.subcode", "None", "" 


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x5f:
   ...     packet.subcode      # None 
   None
 
0x6D - All-In-View Satellite Selection
......................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x6d", ""
   "packet.subcode", "None", "" 


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x6d:
   ...     packet.subcode      # None 
   None
 
0x82 - SBAS Correction Status
.............................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x82", ""
   "packet.subcode", "None", "" 


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x82:
   ...     packet.subcode      # None 
   None
 
0x83 - Double-Precision XYZ Position Fix and Bias Information
.............................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x83", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""
   "packet[1]", "DESC", ""
   "packet[2]", "DESC", ""
   "packet[3]", "DESC", ""
   "packet[4]", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x83:
   ...     packet.subcode      # None 
   None
   ...     packet[0]	#
   1.0
   ...     packet[1]	#
   1.0
   ...     packet[2]	#
   1.0
   ...     packet[3]	#
   1.0
   ...     packet[4]	#
   1.0
 
0x84 - Double-Precision LLA Position Fix and Bias Information
.............................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x84", ""
   "packet.subcode", "None", "" 
   "packet[0]", "DESC", ""
   "packet[1]", "DESC", ""
   "packet[2]", "DESC", ""
   "packet[3]", "DESC", ""
   "packet[4]", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x84:
   ...     packet.subcode      # None 
   None
   ...     packet[0]	#
   1.0
   ...     packet[1]	#
   1.0
   ...     packet[2]	#
   1.0
   ...     packet[3]	#
   1.0
   ...     packet[4]	#
   1.0
 
0x8F-15 - Current Datum Values
..............................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x8f", ""
   "packet.subcode", "0x15", "" 
   "packet[0]", "DESC", ""
   "packet[1]", "DESC", ""
   "packet[2]", "DESC", ""
   "packet[3]", "DESC", ""
   "packet[4]", "DESC", ""
   "packet[5]", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x8f:
   ...     packet.subcode      # 0x15 
   21
   ...     packet[0]	#
   100
   ...     packet[1]	#
   1.0
   ...     packet[2]	#
   1.0
   ...     packet[3]	#
   1.0
   ...     packet[4]	#
   1.0
   ...     packet[5]	#
   1.0
 
0x8F-20 - Last Fix with Extra Information (binary fixed point)
..............................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x8f", ""
   "packet.subcode", "0x20", "" 


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x8f:
   ...     packet.subcode      # 0x20 
   32
 
0x8F-21 - Request Accuracy Information
......................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x8f", ""
   "packet.subcode", "0x21", "" 


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x8f:
   ...     packet.subcode      # 0x21 
   33
 
0x8F-23 - Request Last Compact Fix Information
..............................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x8f", ""
   "packet.subcode", "0x23", "" 
   "packet[0]", "DESC", ""
   "packet[1]", "DESC", ""
   "packet[2]", "DESC", ""
   "packet[3]", "DESC", ""
   "packet[4]", "DESC", ""
   "packet[5]", "DESC", ""
   "packet[6]", "DESC", ""
   "packet[7]", "DESC", ""
   "packet[8]", "DESC", ""
   "packet[9]", "DESC", ""
   "packet[10]", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x8f:
   ...     packet.subcode      # 0x23 
   35
   ...     packet[0]	#
   100
   ...     packet[1]	#
   100
   ...     packet[2]	#
   100
   ...     packet[3]	#
   100
   ...     packet[4]	#
   100
   ...     packet[5]	#
   100
   ...     packet[6]	#
   100
   ...     packet[7]	#
   100
   ...     packet[8]	#
   100
   ...     packet[9]	#
   100
   ...     packet[10]	#
   100
 
0x8F-26 - Non-Volatile Memory Status
....................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x8f", ""
   "packet.subcode", "0x26", "" 


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x8f:
   ...     packet.subcode      # 0x26 
   38
 
0x8F-2A - Fix and Channel Tracking Info, Type 1
...............................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x8f", ""
   "packet.subcode", "0x2a", "" 


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x8f:
   ...     packet.subcode      # 0x2a 
   42
 
0x8F-2B - Fix and Channel Tracking Info, Type 2
...............................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x8f", ""
   "packet.subcode", "0x2b", "" 


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x8f:
   ...     packet.subcode      # 0x2b 
   43
 
0x8F-4F - Set PPS Width
.......................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "packet.code", "0x8f", ""
   "packet.subcode", "0x4f", "" 


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet.code == 0x8f:
   ...     packet.subcode      # 0x4f 
   79

Adding new TSIP packets
~~~~~~~~~~~~~~~~~~~~~~~

The high-level API provides a simple mechanism for adding new TSIP
packets. TODO: Describe this!


Low-Level API
=============

The low-level API can be used to communicate with a Trimble GPS on a 
binary level. This may be useful if a TSIP packet has not been
implemented in the high-level API. The low-level API requires the 
developer to be familiar with the TSIP packet structure and
"byte-stuffing".

The example below encodes TSIP packet 0x1c:0x01 (Command packet 0x1C:01 - Firmware version)
and sends it to the GPS.

.. code-block:: python

   >>> import tsip
   >>> import serial    # pySerial (https://pypi.python.org/pypi/pyserial)
   >>> serial_conn = serial.Serial('/dev/ttyS0', 9600)
   >>> gps_conn = tsip.gps(serial_conn)         # lower-case tsip.gps!
   >>> packet = tsip.frame(tsip.stuff(tsip.DLE + '\x1c\x01' + tsip.DLE + tsip.ETX)
   >>> gps_conn.write(packet)
   >>> while True:      # should implement timeout here!!!
   ...     report = tsip.unstuff(tsip.unframe(gps_conn.read()))
   ...     if report[0] == '\x1c' and report[1] == '\x81':
   ...         print 'Product name: %s' % report[11:]
   ...         break
