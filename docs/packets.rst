TSIP Packets
============

Below is a brief decsription of the TSIP packets supported by *python-TSIP*. For detailed
explanation of the individual fields of each packet refer to the official documentation
available at http://www.trimble.com.


General description
-------------------




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
   
