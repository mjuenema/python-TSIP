python-TSIP
===========

*Python-TSIP* is a Python package for parsing and creating TSIP 
packets. The Trimble Standard Interface Protocol (TSIP) is
the binary protocol spoken by the GPS receivers sold by 
Trimble Navigation Ltd.

TSIP defines approximately 70 dfferent packet types for
configuring and querying Trimble GPS receivers. The *python-TSIP*
package provides a Python class for each type of TSIP packet.


TSIP packet classes
-------------------

The packet classes can be used to either parse a binary TSIP
packet into a Python class instance or generate TSIP packets
from a class instance.

### Example: Generating a TSIP packet

    >>> import tsip
    >>> packet = tsip.ReceiverConfiguration()	# Packet0xBB() 
    >>> packet.receiver_mode = tsip.OVERDETERMINED_CLOCK
    >>> packet.dynamics_code = tsip.STATIONARY
    >>> packet.elevation_mask = tsip.radians(15.0)
    >>> print packet
    >>> str(packet)

### Example: Parsing a TSIP packet

This example uses the `packet` created in the previous example.

    >>> b = str(packet)

The `identify()` function can be used to determine the type of 
TSIP packet. `Packet0xBB` is the same type as `ReceiverConfiguration`,
the latter being an alias for the former.
    
    >>> packet_class = tsip.identify(b)
    >>> packet_class
    tsip.Packet0xBB

Calling the packet class with a single argument will parse the
TSIP packet.

    >>> packet2 = packet_class(s)
    >>> packet2.receiver_mode == tsip.OVERDETERMINED_CLOCK
    True

Parsing TSIP packets is usually not done directly as the feature
is available through the two classes described in the next
section.


GPS interface
-------------

The *python-TSIP* package also provides two classes for communicating
with a Trimble GPS receiver.

The first, `TrimbleGPS`, builds on the `pySerial` package to provide 
read-write communications with a Trimble GPS receiver.

The second class `TrimbleGPSd` connects to a running `gpsd` instance
and requests output in the native TSIP format. This method allows
to share the Trimble GPS with `gpsd` but with read access only.

Both classes implement are Python iterators that return instances of
Python TSIP packet classes.


### Example: `TrimbleGPS`


### Example: `TrimbleGPSd`
