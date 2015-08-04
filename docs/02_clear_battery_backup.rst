================================
Clear battery backup, then reset
================================

Command Packet 0x1e
-------------------

.. class:: Command_1e(reset_mode)

   Command 0x1e commands the receiver to clear all battery back-up
   data followed by a softwware reset. The *reset_mode* can have
   three different values:

   ==== ================================================
   0x4b Cold start: Erase BBRAM and restart
   0x46 Factory reset: Erase BBRAM and Flash and restart
   0x4d Enter monitor mode
   ==== ================================================

Cold start::

   >>> command = Command_1e(0x4b)
   >>> gps_conn.send(command)

Factory reset::

   >>> command = Command_1e(0x46)
   >>> gps_conn.send(command)
