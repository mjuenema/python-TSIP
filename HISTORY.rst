.. :changelog:

History
=======

0.3.2 (28-Oct-2017)
-------------------

* Added Report Packet 0x58: GPS System Data from the Receiver.
* Fixed Report Packet 0x47: Signals Levels for Tracked Satellites.
* Fixed Report Packet 0x6D: Satellite Selection List.x 
* Added `docs/examples/example2.py` wich provides a more comprehensive
  template program than the example in the README.

0.3.1 (26-Sep-2017)
-------------------

* Fixed README.rst so it renders properly on PyPi.

0.3.0 (26-Sep-2017)
-------------------

* Argument to ``tsip.Packet()`` can now also be a tuple or list 
  (inspired by Criss Swaim).
* Changed development status from alpha to beta.
* Cleaned up lots of code to satisfy flake8.

0.2.0 (03-Dec-2015)
-------------------

* Rewritten from scratch.
* Implements almost complete set of TSIP commands supported by
  Trimble Copernicus II and Thunderbolt/Thunderbolt-E GPS
  receivers.

0.1.0 (20-Jun-2015)
---------------------

* First release on PyPI.
