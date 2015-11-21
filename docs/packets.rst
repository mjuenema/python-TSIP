TSIP Packets
============

Below is a brief decsription of the TSIP packets supported by *python-TSIP*. For detailed
explanation of the individual fields of each packet refer to the official documentation
available at http://www.trimble.com.


General description
-------------------


Command Packet 0x1C - Firmware Version 01
-----------------------------------------

.. csv-table:: 
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30
   
   "packet.code", "Packet ID (0x1c)", ""
   "packet.subcode", "0x01", ""  


Report packet 0x1C:81 - Report firmware version
-----------------------------------------

.. csv-table:: 
   :header: "Field", "Description", "Notes"
   :widths: 10, 20, 30
   
   "packet.code", "Packet ID (0x1c)", ""
   "packet.subcode", "0x81", ""
   "packet[0]", "(reserved)", ""
   "packet[1]", "major version", ""
   "packet[2]", "minor version", ""
   "packet[3]", "build number", ""
   "packet[4]", "month", ""
   "packet[5]", "day", ""
   "packet[6]", "year", "as a four-digit number, e.g. 2015"
   "packet[7]", "product name", "byte 10 ('length of first module name') is skipped"


Packet 0xBB: Receiver Configuration
-----------------------------------

Packet 0xbb contains multiple fields that (must) always contain 0xff and the official 
documentation warns "do not alter". *python-TSIP* will force these fields to ``0xff`` before
a packet is being send to the GPS. 

When changing the receiver configuration these fields must 
not be skipped when creating a Packet although it is possible to omit the trailing 
(after "Foliage Mode") ``0xff`` values. Any settings that shall remain unchanged must have
their field set to ``0xff`` for integers or ``-1.0`` for floats.  

Set "Dynamics Code" to "Stationary(4)" and "Foliage Mode" to "Sometimes(1)". Leave all other
settings unchanged. Then query the current settings.

.. code-block:: python

   command = Packet(0xbb, 0x00, 0xff, 4, 0xff, -0.1, -0.1, -0.1, 0xff, 1)
   gps.write(command)

   command = Packet(0xbb, 0x00)
   gps.write(packet)
   report = gps.read()
   
   if report.code == 0xbb and report.subcode == 0:
       print report
   # 
   
