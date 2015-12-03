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
   ...         if report[0] == 0x41:
   ...             print 'GPS time of week .......: %f' % (report[1])
   ...             print 'Extended GPS week number: %d' % (report[2])
   ...             print 'GPS UTC offset .........: %f' % (report[3])
   ...             break

Instances of `tsip.GPS` can also be iterated over.

.. code-block:: python

   >>> for packet in gps_conn:
   ...     print packet[0]
   


TSIP Packets (`tsip.Packet` class)
----------------------------------

Not all Trimble GPS receivers support all TSIP packets.
Check the official documentation for more details and additional information.

.. warning:: This section is not up-to-date.


Command Packets
~~~~~~~~~~~~~~~
 
0x1C - Firmware Version 01
..........................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x1c", ""
   "1", "0x01", "" 

.. literalinclude:: examples/0x1c01.py
   :lines: 3-


0x1C - Firmware Version 03
..........................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x1c", ""
   "1", "0x03", "" 


.. code-block:: python

   >>> command = Packet(0x1c, 0x03)
   >>> command[0]  # 0x1c
   28
   >>> command[1]  # 0x03
   3
   >>> gps_conn.write(command)
   >>> while True:
   ...     report = gps_conn.read()
   ...     if report[0] == 0x1c and report.subcode == 0x83:
   ...         print report
   ...         break
   Packet(0x1c, 0x83, ...)

 
0x1E - Clear Battery Backup, then Reset
.......................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x1e", ""
   "1", "Reset type", ""


.. code-block:: python

   >>> command = Packet(0x1e, 0x46)    # 0x46 = factory reset
   >>> command[0]  # 0x1e
   30
   >>> command[1]  # 0x46
   70
   >>> gps_conn.write(command)

 
0x1F - Request Software Versions
................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x1f", ""


.. code-block:: python

   >>> command = Packet(0x1f)
   >>> command[0]  # 0x1f
   31
   >>> gps_conn.write(command)
   >>> while True:
   ...     report = gps_conn.read()
   ...     if report[0] == 0x45:
   ...         print report
   ...         break
   Packet(0x45, ...)

 
0x21 - Request Current Time
...........................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x21", ""


.. code-block:: python

   >>> command = Packet(0x21)
   >>> command[0]  # 0x21
   33
   >>> gps_conn.write(command)
   >>> while True:
   ...     report = gps_conn.read()
   ...     if report[0] == 0x41:
   ...         print report
   ...         break
   Packet(0x41, ...)

 
0x23 - Initial Position (XYZ ECEF)
..................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x23", ""
   "1", "X", ""
   "2", "Y", ""
   "3", "Z", ""


.. code-block:: python

   >>> packet = Packet(0x23, -4130.889, 2896.451, -3889.139)
   >>> packet[0]        # 0x23
   35
   >>> packet[1]        # X
   -4130.889
   >>> packet[2]        # Y
   2896.451
   >>> packet[3]        # Z
   -3889.139
   >>> gps_conn.write(command)

 
0x24 - Request GPS Receiver Position Fix Mode
.............................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x24", ""


.. code-block:: python

   >>> command = Packet(0x24)
   >>> command[0]       # 0x24
   36
   >>> gps_conn.write(command)
   >>> while True:
   ...     report = gps_conn.read()
   ...     if report[0] == 0x6d:
   ...         print report
   ...         break
   Packet(0x6d

 
0x25 - Initiate Soft Reset & Self Test
......................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x25", ""


.. code-block:: python

   >>> command = Packet(0x25)
   >>> command[0]       # 0x25
   37
   >>> gps_conn.write(command)

 
0x26 - Request Health
.....................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x26", ""


.. code-block:: python

   >>> command = Packet(0x26)
   >>> command[0]       # 0x26
   38
   >>> gps_conn.write(command)
   >>> while True:
   ...     report = gps_conn.read()
   ...     if report[0] == 0x46 or report[0] == 0x4b:
   ...         print report
   ...         break
   Packet(0x4b

 
0x27 - Request Signal Levels
............................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x27", ""


.. code-block:: python

   >>> command = Packet(0x27)
   >>> command[0]     # 0x27
   39
   >>> gps_conn.write(command)
   >>> while True:
   ...     report = gps_conn.read()
   ...     if report[0] == 0x47:
   ...         print report
   ...         break
   Packet(0x47


 
0x2B - Initial Position (Latitude, Longitude, Altitude)
.......................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x2b", ""
   "1", "Latitude", ""
   "2", "Longitude", ""
   "3", "Alitude", ""


.. code-block:: python

   >>> import maths
   >>> packet = Packet(0x2b, math.radians(-37.813611), math.radians(144.963056), 30.0)
   >>> packet[0]     # 0x2b
   43
   >>> packet[1]     # radians
   -0.6599720140183456
   >>> packet[2]     # radians
   2.5300826209529208
   >>> packet[0]     # metres
   30.0
   >>> gps_conn.write(command)

 
0x2D - Request Oscillator Offset
................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x2d", ""


.. code-block:: python

   >>> packet = Packet(0x2d)
   >>> packet[0]     # 0x2d
   45
   >>> gps_conn.write(command)
   >>> while True:
   ...     report = gps_conn.read()
   ...     if report[0] == 0x4d:
   ...         print report
   ...         break
   Packet(0x4d

 
0x2E - Set GPS Time
...................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x2e", ""
   "1", "GPS time of week", "" 
   "2", "Extended GPS week number", ""


.. code-block:: python

   >>> packet = Packet(0x2e,
   >>> packet[0]     # 0x2e
   46
   >>> gps_conn.write(command)

 
0x31 - Accurate Initial Position (XYZ ECEF)
...........................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x31", ""
   "1", "Latitude", ""
   "2", "Longitude", ""
   "3", "Alitude", ""

.. code-block:: python

   >>> packet = Packet(0x2b, math.radians(-37.813611), math.radians(144.963056), 30.0)
   >>> packet[0]     # 0x31
   49
   >>> packet[1]     # radians
   -0.6599720140183456
   >>> packet[2]     # radians
   2.5300826209529208
   >>> packet[0]     # metres
   30.0
   >>> gps_conn.write(command)

.. TODO continue here

 
0x32 - Accurate Initial Position, (Latitude, Longitude, Altitude)
.................................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x32", ""
   "1", "None", "" 
   "2", "DESC", ""
   "3", "DESC", ""
   "4", "DESC", ""


.. code-block:: python

   >>> packet = Packet(0x32, 1.0, 1.0, 1.0)
   >>> packet[0]     # 0x32
   50

 
0x35 - Set Request I/O Options
..............................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x35", ""
   "1", "None", "" 
   "2", "DESC", ""
   "3", "DESC", ""
   "4", "DESC", ""
   "5", "DESC", ""


.. code-block:: python

   >>> packet = Packet(0x35, 100, 100, 100, 100)
   >>> packet[0]     # 0x35
   53

 
0x37 - Request Status and Values of Last Position and Velocity
..............................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x37", ""
   "1", "None", "" 


.. code-block:: python

   >>> packet = Packet(0x37)
   >>> packet[0]     # 0x37
   55

 
0x38 - Request/Load Satellite System Data
.........................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x38", ""
   "1", "None", "" 
   "2", "DESC", ""
   "3", "DESC", ""
   "4", "DESC", ""


.. code-block:: python

   >>> packet = Packet(0x38, 100, 100, 100)
   >>> packet[0]     # 0x38
   56

 
0x3A - Request Last Raw Measurement
...................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x3a", ""
   "1", "None", "" 
   "2", "DESC", ""


.. code-block:: python

   >>> packet = Packet(0x3a, 100)
   >>> packet[0]     # 0x3a
   58

 
0x3C - Request Current Satellite Tracking Status
................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x3c", ""
   "1", "None", "" 
   "2", "DESC", ""


.. code-block:: python

   >>> packet = Packet(0x3c, 100)
   >>> packet[0]     # 0x3c
   60

 
0x69 - Receiver Acquisition Sensitivity Mode
............................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x69", ""
   "1", "None", "" 


.. code-block:: python

   >>> packet = Packet(0x69)
   >>> packet[0]     # 0x69
   105

 
0x7E - TAIP Message Output
..........................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x7e", ""
   "1", "None", "" 


.. code-block:: python

   >>> packet = Packet(0x7e)
   >>> packet[0]     # 0x7e
   126

 
0x8E-17 - Request Last Position or Auto-Report Position in UTM Single Precision Format
......................................................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x8e", ""
   "1", "0x17", "" 


.. code-block:: python

   >>> packet = Packet(0x8e, 0x17)
   >>> packet[0]     # 0x8e
   142
   >>> packet[1]  # 0x17
   23


 
0x8E-20 - Request Last Fix with Extra Information
.................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x8e", ""
   "1", "0x20", "" 


.. code-block:: python

   >>> packet = Packet(0x8e, 0x20)
   >>> packet[0]     # 0x8e
   142
   >>> packet[1]  # 0x20
   32


 
0x8E-21 - Request Accuracy Information
......................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x8e", ""
   "1", "0x21", "" 


.. code-block:: python

   >>> packet = Packet(0x8e, 0x21)
   >>> packet[0]     # 0x8e
   142
   >>> packet[1]  # 0x21
   33


 
0x8E-23 - Request Last Compact Fix Information
..............................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x8e", ""
   "1", "0x23", "" 
   "2", "DESC", ""


.. code-block:: python

   >>> packet = Packet(0x8e, 0x23, 100)
   >>> packet[0]     # 0x8e
   142
   >>> packet[1]  # 0x23
   35


 
0x8E-26 - Non-Volatile Memory Storage
.....................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x8e", ""
   "1", "0x26", "" 


.. code-block:: python

   >>> packet = Packet(0x8e, 0x26)
   >>> packet[0]     # 0x8e
   142
   >>> packet[1]  # 0x26
   38


 
0x8E-2A - Request Fix and Channel Tracking Info, Type 1
.......................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x8e", ""
   "1", "0x2a", "" 


.. code-block:: python

   >>> packet = Packet(0x8e, 0x2a)
   >>> packet[0]     # 0x8e
   142
   >>> packet[1]  # 0x2a
   42


 
0x8E-2B - Request Fix and Channel Tracking Info, Type 2
.......................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x8e", ""
   "1", "0x2b", "" 


.. code-block:: python

   >>> packet = Packet(0x8e, 0x2b)
   >>> packet[0]     # 0x8e
   142
   >>> packet[1]  # 0x2b
   43


 
0x8E-4F - Set PPS Width
.......................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x8e", ""
   "1", "0x4f", "" 


.. code-block:: python

   >>> packet = Packet(0x8e, 0x4f)
   >>> packet[0]     # 0x8e
   142
   >>> packet[1]  # 0x4f
   79


 
0xBB - Navigation Configuration
...............................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0xbb", ""
   "1", "None", "" 


.. code-block:: python

   >>> packet = Packet(0xbb)
   >>> packet[0]     # 0xbb
   187

 
0xBC - Protocol Configuration
.............................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0xbc", ""
   "1", "None", "" 
   "2", "DESC", ""


.. code-block:: python

   >>> packet = Packet(0xbc, 100)
   >>> packet[0]     # 0xbc
   188

 
0xC0 - Graceful Shutdown and Go To Standby Mode
...............................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0xc0", ""
   "1", "None", "" 


.. code-block:: python

   >>> packet = Packet(0xc0)
   >>> packet[0]     # 0xc0
   192

 
0xC2 - SBAS SV Mask.
....................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0xc2", ""
   "1", "None", "" 


.. code-block:: python

   >>> packet = Packet(0xc2)
   >>> packet[0]     # 0xc2
   194

Report Packets
~~~~~~~~~~~~~~
 
0x41 - GPS Time
...............

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x41", ""
   "1", "None", "" 
   "2", "DESC", ""
   "3", "DESC", ""
   "4", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x41:
   ...     packet[1]	#
   1.0
   ...     packet[2]	#
   100
   ...     packet[3]	#
   1.0
 
0x42 - Single-Precision Position Fix, XYZ ECEF
..............................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x42", ""
   "1", "None", "" 
   "2", "DESC", ""
   "3", "DESC", ""
   "4", "DESC", ""
   "5", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x42:
   ...     packet[1]	#
   1.0
   ...     packet[2]	#
   1.0
   ...     packet[3]	#
   1.0
   ...     packet[4]	#
   1.0
 
0x43 - Velocity Fix, XYZ ECEF
.............................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x43", ""
   "1", "None", "" 
   "2", "DESC", ""
   "3", "DESC", ""
   "4", "DESC", ""
   "5", "DESC", ""
   "6", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x43:
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
 
0x45 - Software Version Information
...................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x45", ""
   "1", "DESC", ""
   "2", "DESC", ""
   "3", "DESC", ""
   "4", "DESC", ""
   "5", "DESC", ""
   "6", "DESC", ""
   "7", "DESC", ""
   "8", "DESC", ""
   "9", "DESC", ""
   "10", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x45:
   ...     packet[1]    # 
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
 
0x46 - Health of Receiver
.........................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x46", ""
   "1", "None", "" 
   "2", "DESC", ""
   "3", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x46:
   ...     packet[1]      # None 
   None
   ...     packet[2]	#
   100
   ...     packet[3]	#
   100
 
0x47 - Signal Levels for all Satellites
.......................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x47", ""
   "1", "None", "" 
   "2", "DESC", ""
   "3", "DESC", ""
   "4", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x47:
   ...     packet[1]      # None 
   None
   ...     packet[2]	#
   100
   ...     packet[3]	#
   100
   ...     packet[4]	#
   1.0
 
0x4A - Single Precision LLA Position Fix
........................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x4a", ""
   "1", "None", "" 
   "2", "DESC", ""
   "3", "DESC", ""
   "4", "DESC", ""
   "5", "DESC", ""
   "6", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x4a:
   ...     packet[1]      # None 
   None
   ...     packet[2]	#
   1.0
   ...     packet[3]	#
   1.0
   ...     packet[4]	#
   1.0
   ...     packet[5]	#
   1.0
   ...     packet[6]	#
   1.0
 
0x4B - Machine/Code ID and Additional Status
............................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x4b", ""
   "1", "None", "" 
   "2", "DESC", ""
   "3", "DESC", ""
   "4", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x4b:
   ...     packet[1]      # None 
   None
   ...     packet[2]	#
   100
   ...     packet[3]	#
   100
   ...     packet[4]	#
   100
 
0x4D - Oscillator Offset
........................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x4d", ""
   "1", "None", "" 
   "2", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x4d:
   ...     packet[1]      # None 
   None
   ...     packet[2]	#
   1.0
 
0x4E - Response to Set GPS Time
...............................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x4e", ""
   "1", "None", "" 


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x4e:
   ...     packet[1]      # None 
   None
 
0x55 - I/O Options
..................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x55", ""
   "1", "None", "" 
   "2", "DESC", ""
   "3", "DESC", ""
   "4", "DESC", ""
   "5", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x55:
   ...     packet[1]      # None 
   None
   ...     packet[2]	#
   100
   ...     packet[3]	#
   100
   ...     packet[4]	#
   100
   ...     packet[5]	#
   100
 
0x56 - Velocity Fix, East-North-Up (ENU)
........................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x56", ""
   "1", "None", "" 
   "2", "DESC", ""
   "3", "DESC", ""
   "4", "DESC", ""
   "5", "DESC", ""
   "6", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x56:
   ...     packet[1]      # None 
   None
   ...     packet[2]	#
   1.0
   ...     packet[3]	#
   1.0
   ...     packet[4]	#
   1.0
   ...     packet[5]	#
   1.0
   ...     packet[6]	#
   1.0
 
0x57 - Information About Last Computed Fix
..........................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x57", ""
   "1", "None", "" 
   "2", "DESC", ""
   "3", "DESC", ""
   "4", "DESC", ""
   "5", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x57:
   ...     packet[1]      # None 
   None
   ...     packet[2]	#
   100
   ...     packet[3]	#
   100
   ...     packet[4]	#
   1.0
   ...     packet[5]	#
   100
 
0x58 - Satellite System Data/Acknowledge from Receiver
......................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x58", ""
   "1", "None", "" 


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x58:
   ...     packet[1]      # None 
   None
 
0x5A - Raw Measurement Data
...........................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x5a", ""
   "1", "None", "" 
   "2", "DESC", ""
   "3", "DESC", ""
   "4", "DESC", ""
   "5", "DESC", ""
   "6", "DESC", ""
   "7", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x5a:
   ...     packet[1]      # None 
   None
   ...     packet[2]	#
   100
   ...     packet[3]	#
   1.0
   ...     packet[4]	#
   1.0
   ...     packet[5]	#
   1.0
   ...     packet[6]	#
   1.0
   ...     packet[7]	#
   1.0
 
0x5C - Satellite Tracking Status
................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x5c", ""
   "1", "None", "" 
   "2", "DESC", ""
   "3", "DESC", ""
   "4", "DESC", ""
   "5", "DESC", ""
   "6", "DESC", ""
   "7", "DESC", ""
   "8", "DESC", ""
   "9", "DESC", ""
   "10", "DESC", ""
   "11", "DESC", ""
   "12", "DESC", ""
   "11", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x5c:
   ...     packet[1]      # None 
   None
   ...     packet[2]	#
   100
   ...     packet[3]	#
   100
   ...     packet[4]	#
   100
   ...     packet[5]	#
   100
   ...     packet[6]	#
   1.0
   ...     packet[7]	#
   1.0
   ...     packet[8]	#
   1.0
   ...     packet[9]	#
   1.0
   ...     packet[10]	#
   100
   ...     packet[11]	#
   100
   ...     packet[12]	#
   100
   ...     packet[11]	#
   100
 
0x5F - Diagnostic Use Only
..........................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x5f", ""
   "1", "None", "" 


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x5f:
   ...     packet[1]      # None 
   None
 
0x6D - All-In-View Satellite Selection
......................................
  

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x6d", ""
   "1", "Dimension", "" 
   "2", "PDOP", ""
   "3", "HDOP", ""
   "4", "VDOP", ""
   "5", "TDOP", ""
   "x", "SV PRN", ""


.. code-block:: python

   >>> report = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if report[0] == 0x6d:
   ...     print report      
   Packet(0x6d, 3, 10.0, 20.0, 30.0, 40.0, -1, -2, 3)
   ...     print 'SV in view: %s' % (report[6:])
   SV in view: [-1, -2, 3]
 
0x82 - SBAS Correction Status
.............................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x82", ""
   "1", "SBAS status bits", "" 


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x82:
   ...     packet[1]
   2
 
0x83 - Double-Precision XYZ Position Fix and Bias Information
.............................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x83", ""
   "1", "None", "" 
   "2", "DESC", ""
   "3", "DESC", ""
   "4", "DESC", ""
   "5", "DESC", ""
   "6", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x83:
   ...     packet[1]      # None 
   None
   ...     packet[2]	#
   1.0
   ...     packet[3]	#
   1.0
   ...     packet[4]	#
   1.0
   ...     packet[5]	#
   1.0
   ...     packet[6]	#
   1.0
 
0x84 - Double-Precision LLA Position Fix and Bias Information
.............................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x84", ""
   "1", "None", "" 
   "2", "DESC", ""
   "3", "DESC", ""
   "4", "DESC", ""
   "5", "DESC", ""
   "6", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x84:
   ...     packet[1]      # None 
   None
   ...     packet[2]	#
   1.0
   ...     packet[3]	#
   1.0
   ...     packet[4]	#
   1.0
   ...     packet[5]	#
   1.0
   ...     packet[6]	#
   1.0
 
0x8F-15 - Current Datum Values
..............................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x8f", ""
   "1", "0x15", "" 
   "2", "DESC", ""
   "3", "DESC", ""
   "4", "DESC", ""
   "5", "DESC", ""
   "6", "DESC", ""
   "7", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x8f:
   ...     packet[1]      # 0x15 
   21
   ...     packet[2]	#
   100
   ...     packet[3]	#
   1.0
   ...     packet[4]	#
   1.0
   ...     packet[5]	#
   1.0
   ...     packet[6]	#
   1.0
   ...     packet[7]	#
   1.0
 
0x8F-20 - Last Fix with Extra Information (binary fixed point)
..............................................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x8f", ""
   "1", "0x20", "" 


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x8f:
   ...     packet[1]      # 0x20 
   32
 
0x8F-21 - Request Accuracy Information
......................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x8f", ""
   "1", "0x21", "" 


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x8f:
   ...     packet[1]      # 0x21 
   33
 
0x8F-23 - Request Last Compact Fix Information
..............................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x8f", ""
   "1", "0x23", "" 
   "2", "DESC", ""
   "3", "DESC", ""
   "4", "DESC", ""
   "5", "DESC", ""
   "6", "DESC", ""
   "7", "DESC", ""
   "8", "DESC", ""
   "9", "DESC", ""
   "10", "DESC", ""
   "11", "DESC", ""
   "12", "DESC", ""


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x8f:
   ...     packet[1]      # 0x23 
   35
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
   ...     packet[11]	#
   100
   ...     packet[12]	#
   100
 
0x8F-26 - Non-Volatile Memory Status
....................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x8f", ""
   "1", "0x26", "" 


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x8f:
   ...     packet[1]      # 0x26 
   38
 
0x8F-2A - Fix and Channel Tracking Info, Type 1
...............................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x8f", ""
   "1", "0x2a", "" 


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x8f:
   ...     packet[1]      # 0x2a 
   42
 
0x8F-2B - Fix and Channel Tracking Info, Type 2
...............................................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x8f", ""
   "1", "0x2b", "" 


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x8f:
   ...     packet[1]      # 0x2b 
   43
 
0x8F-4F - Set PPS Width
.......................

.. csv-table::
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30

   "0", "0x8f", ""
   "1", "0x4f", "" 


.. code-block:: python

   >>> packet = gps.read()
   >>> isinstance(packet, tsip.Packet)
   True
   >>> if packet[0] == 0x8f:
   ...     packet[1]      # 0x4f 
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
