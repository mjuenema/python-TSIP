==========================
Version information (0x1c)
==========================

Command packet 0x1c
-------------------

.. class:: Command_1c(subcode)

   The command packet 0x1c may be issued to obtain version information.
   The *subcode* determines whether firmware version (1) or hardware
   version (3) information is requested. The GPS replies with a
   :class:`Report_1c()` packet with its :attribute:`Report_1c.subcode` set
   to 81 or 83, depending on what information was requested.

Report packet 0x1c
------------------

.. class:: Report_1c()

   :class:`Report_1c()` contains the information requested by a
   :class:`Command_1c()` packet. The :attribute:`subcode` must be
   checked to determine whether the report contains firmware version
   information (81) or hardware version information (83). 

   .. attribute:: subcode

   If :attribute:`subcode` equals 81, then the following attributes
   provide firmware version information.

   .. attribute:: major_version

      Firmware major version as an integer.

   .. attribute:: minor_version

      Firmware minor version as an integer.

   .. attribute:: build_number

      Firmware build number as an integer.

   .. attribute:: version

      The combination of :attribute:`major_version`, :attribute:`minor_version`
      and :attribute:`build_number` as a string.

   .. attribute:: build_date

      The firmware build date as a :class:`datetime.date()` instance.

   .. attribute:: product_name

      The product name as a string.

   If :attribute:`subcode` equals 83, then the following attributes
   provide hardware version information.

   .. attribute:: serial_number

      The board serial number as an integer.

   .. attribute:: build_date

      The board's build date as a :class:`datetime.datetime()` instance.

   .. attribute:: hardware_code

      The hardware code as an integer.

   .. attribute:: hardware_id

      The hardware ID as an ASCII string.

  
Firmware version example::

   >>> command = Command_1c(1)
   >>> gps_conn.send(command)
   >>> report = gps_conn.read()
   >>> if report.code == 0x1c and report.subcode == 81:
   ...    print report.major_version
   TODO
   ...    print report.minor_version
   TODO
   ...    print report.build_number
   TODO
   ...    print report.version
   TODO
   ...    print report.product_name
   TODO

Hardware version example::

   >>> command = Command_1c(3)
   >>> gps_conn.send(command)
   >>> report = gps_conn.read()
   >>> if report.code == 0x1c and report.subcode == 83:
   ...    print report.serial_number
   TODO
   ...    print report.build_date
   TODO
   ...    print report.hardware_code
   TODO
   ...    print report.hardware_id
   TODO
