Overview of TSIP packets
------------------------

Regular TSIP packets
~~~~~~~~~~~~~~~~~~~~

======== === =================================== ==== =========================
Code     C/R Description                         Impl Notes
======== === =================================== ==== =========================
0x13       R Unparseable packet                  
0x1C     C+R Version information                 
0x21     C   Query GPS time
0x23     C   Set approximate XYZ ECEF
0x24     C   Query satellite selection
0x25     C   Soft reset
0x26     C   Query receiver ID and error status
0x27     C   Query signal levels
0x2B     C   Set approximate LLA
0x2E     C   Set GPS time
0x31     C   Set exact ZYC ECEF
0x32     C   Set exact LLA
0x35     C   Set IO options       
0x38     C   Query load GPS system data
0x3C     C   Query satellite information
0x41       R Report GPS time                     yes
0x43       R XYZ ECEF velocity
0x45       R Software version                         
0x46       R Receiver health
0x4B       R Machine code/status                 yes
0x4E       R Report GPS time
0x55       R Report IO options
0x56       R ENU velocity
0x6D       R Report satellite selection          yes
0x7A     C+R NMEA configuration
0x82         SBAS fix mode
0x83       R Double-precision XYZ ECEF
0x84       R Double-precision LLA
0xBB     C+R receiver configuration
0xBC     C+R Port configuration
======== === =================================== ==== =========================

C/R
    Command and/or report packet.

Impl
    Implemented in Python-TSIP.

TSIP super-packets
~~~~~~~~~~~~~~~~~~

======== === =================================== ==== =========================
Code     C/R Description                         Impl Notes
======== === =================================== ==== =========================
0x8F20   C+R Position and velocity
======== === =================================== ==== =========================

C/R
    Command and/or report packet.

Impl
    Implemented in Python-TSIP.

Commands and reports.

========== ========== ====================================================
Command    Report     Description
========== ========== ====================================================
0x1c (01)  0x1c (81)  Firmware version (01)
0x1c (03)  0x1c (83)  Firmware version (83)
0x1e                  Clear battery backup, then reset
0x1f       0x45       Software version
0x21       0x41       Current GPS time
0x23                  Initial position (XYZ ECEF)
0x24       0x6d       GPS receiver position fix mode
0x25       0x45       Soft reset and self-test
0x26       0x46       Health
0x26       0x4b       Health
0x27       0x47       Signal levels
0x2b                  Initial position (LLA)
0x2d       0x4d       Oscillator offset
0x2e       0x4e       Set GPS time
0x31                  Accurate initial position (XYZ ECEF)
0x32                  Accurate initial position (LLA)
0x35       0x55       I/O options (set automatic output packets) 
0x37       0x57       Status and latest position and velocity
0x38       0x58       Satellite system data
0x3a       0x5a       Raw measurement
0x3c       0x5c       Current satellite tracking status
.          0x42       Single preecision fix (XYZ ECEF)
.          0x43       Velocity fix (XYZ ECEF)
.          0x4a       Single preecision fix (LLA)
.          0x56       Velocity fix (ENU)
.          0x5f       Trimble diagnostics
0x69       0x89       Receiver acquisition sensitivity mode
0x7a       0x7b       NMEA settings and interval
0x7e                  TAIP message output
.          0x82       SBAS correction status
.          0x83       Double precision fix (XYZ ECEF)
.          0x84       Double precision fix (LLA)
0xbb       0xbb       Navigation configuration
0xbc       0xbc       Protocol configuration
0xc0                  Graceful shutdown and go to standby mode
0xc2                  SBAS SV mask
========== ========== ====================================================

TSIP super-packet commands and reports.

========== ========== ====================================================
Command    Report     Description
========== ========== ====================================================
0x8e15     0x8f15     Datum
0x8e17     0x8f17     Last position in UTM single precision format
0x8e18     0x8f18     Last position in UTM double precision format
0x8e20     0x8f20     Last position with extra information
0x8e21     0x8f21     Accuracy information
0x8e23     0x8f23     Last compact fix information
0x8e26     0x8f26     Non-volatile memory storage
0x8e2a     0x8f2a     Fix and channel tracking info (type 1)
0x8e2b     0x8f2b     Fix and channel tracking info (type 2)
0x8e4a     0x8f4a     Copernicus II GPS receiver delay and polarity
0x8e4f     0x8f4f     PPS width
========== ========== ====================================================


