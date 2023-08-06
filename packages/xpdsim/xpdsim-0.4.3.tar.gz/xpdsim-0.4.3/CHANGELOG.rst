=================
xpdSim Change Log
=================

.. current developments

v0.4.3
====================



v0.4.2
====================



v0.4.1
====================

**Added:**

* Factory method for creating simulated area detectors with
     user-supplied image sequence. Useful for testing analysis
      pipelines on specific sample/experiment conditions.

**Fixed:**

* Syntax of simulated ophyd object. Aligned with current NSLS-II
    development.



v0.4.0
====================

**Added:**

* new area detector who's value is coupled to a mover

**Fixed:**

* Cast detectors into float32 before sending data out



v0.3.0
====================

**Added:**

* ``blackfly`` detector and an associated ``blackfly_full_field`` det



v0.2.0
====================

**Added:**

* Capacity to change the name for area detectors
* ``xpd_pe2c`` detector

**Changed:**

* The area detector now uses the shutter by default
* The area detector now writes into a temp dir with a prefix (making removal
  easier)
* Add poisson noise to the detector



v0.1.5
====================

**Fixed:**

* ``pyfai_poni`` now is properly stored in package data.




v0.1.4
====================



v0.1.3
====================

**Added:**

* Poni file in ``__init__.py``

* Direct image file location in ``__init__.py``




v0.1.2
====================

**Added:**

* Filterbank




v0.1.1
====================

**Added:**

* Add rever releaser




