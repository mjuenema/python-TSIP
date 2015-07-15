=====
Usage
=====

Reading from a GPS
------------------

The example below reads TSIP packets from a Trimble GPS
connected to serial port ``/dev/ttyS0``. This requires the
pySerial_ package.

.. _pySerial_: http://pyserial.sourceforge.net/

.. code-block:: python

    from serial import Serial
    from tsip import GPS

    serial_conn = serial.Serial('/dev/ttyS0', 9600)
    gps_conn = GPS(serial_conn)

    while True:
        packet = gps.read()

        # 0x8f23 - Compact Fix Information
        if packet.code == 0x8f23:
            print packet.latitude
            print packet.longitude
            print packet.altitude


Alternatively to calling ``gps.read()`` over and over again
it is also possible to iterate over the ``GPS`` instance.

.. code-block:: python

    from serial import Serial
    from tsip import GPS

    serial_conn = serial.Serial('/dev/ttyS0', 9600)
    gps_conn = GPS(serial_conn)

    for packet in gps:

        # 0x8f23 - Compact Fix Information
        if packet.code == 0x8f23:
            print packet.latitude
            print packet.longitude
            print packet.altitude


Check the API and official Trimble documentation for details.


Sending commands to a GPS
-------------------------

It is also possible to send commands to the GPS. There is a 
Python class for many TSIP commands.
    

.. code-block:: python

    from serial import Serial
    from tsip import GPS
    from tsip import Command_32    # 0x32 - Set accurate initial position

    serial_conn = serial.Serial('/dev/ttyS0', 9600)
    gps_conn = GPS(serial_conn)

    cmd = Command_32(-37.813611, 144.963056, 25.0)
    gps_conn.send(cmd)


Check the API and official Trimble documentation for details.
