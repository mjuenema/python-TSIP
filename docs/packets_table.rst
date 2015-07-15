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
