python-TSIP
===========

**This project had been idle for a long time until very recently. The
previous version of this README described an API that I originally 
intended to implement. This has now been abandoned in favour of a
much easier to implement API as described below. Still, at this
stage all this just exists in my head.**

*Python-TSIP* is a Python package for parsing and creating TSIP 
packets. The Trimble Standard Interface Protocol (TSIP) is
the binary protocol spoken by the GPS receivers sold by 
[Trimble Navigation Ltd.](http://www.trimble.com).


Connecting to a GPS
-------------------

*Python-TSIP* relies on an existing connection to a GPS. This
connection object must provide ```.read(n)``` and ```.write(data)```
methods. The [pySerial](http://pyserial.sourceforge.net/)
package can be used to access Trimble GPS connected to a serial
port. 

```python
>>> import serial
>>> serconn = serial.Serial('/dev/ttyS1', 9600)

>>> import tsip
>>> gpsconn = tsip.TSIP(serconn)
```

Communicating with a GPS
------------------------

Once connection is established, one can either use the ```TSIP.read()``` method
to read the next TSIP report or simply iterate over the received TSIP reports.
The contained fields are accessible by numeric index.

```python
>>> for report in gpsconn:
...     if report.code == 0x8f20:	# Last fix with extra info
...         latitude = report[7]
...         longitude = report[8]
```

Sending commands to the GPS is also possible. 

```python
>>> packet = tsip.Command(0x1e, 0x46)	# Erase NVRAM and flash and restart
>>> gpsonn.write(packet)
```
