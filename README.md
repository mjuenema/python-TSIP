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

With some trickery it should also be possible to use the raw (TSIP)
output of a [gpsd](http://www.catb.org/gpsd/) instance 
talking to a Trimble GPS but I haven't actually tested this yet.

```python
>>> import socket
>>> sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
>>> sock.connect(("localhost", 2947))
>>> sockfp = sock.makefile()
>>> sock.send('?WATCH={"raw": 1, "enable": true}\n')

>>> import tsip
>>> gpsconn = tsip.TSIP(serconn)

```


Communication with a GPS
------------------------

Once connection is established, one can either use the ```TSIP.read()``` method
to read the next TSIP packet or simply iterate over the received TSIP packets.
The returned packet has already been parsed and the contained fields are
accessible by numeric index.

```python
>>> for packet in gpsconn:
...     if packet.code == 0x8f20:	# Last fix with extra info
...         latitude = packet[7]
...         longitude = packet[8]
```

Sending packets to the GPS is also possible. 

```python
>>> packet = tsip.Packet(0x1d, 0x46)	# Erase NVRAM and flash and restart
>>> gpsonn.write(packet)
```
