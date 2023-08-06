``xpdsim`` installation guide
=============================

Before starting, make sure ``anaconda`` is installed, it is required for this installation. Note the syntax of this installation guide, as it was written, is based on Uinux system. For Windows users, please change the syntax accordingly if needed.

#. Activate/create a ``python3`` conda environment

#. Install ``XPD`` stack from your terminal

   .. code-block:: none

      conda install -c conda-forge ipython xpdsim xpdacq xpdan

#. Setting up ``ipython`` profile

   #. Create ``collection`` profile from your terminal

      .. code-block:: none

         ipython profile create collection

   #. Download the configuration file `999-load.py <https://github.com/xpdAcq/xpdAcq/blob/master/xpdacq/999-load.py>`_ from `xpdAcq` repo.

   #. Copy and paste the configuration file into the `startup` directory of ipython `collection` profile: ``~/.ipython/profile_collection/startup/``.

      Note ``~/`` means the home directory of your machine, which depends on your OS and machine status. You can find out the exact filepath of ``~`` by doing the following in a ``Python`` session

         .. code-block:: python

            import os
            os.path.expanduser('~')

      More information about the ``ipython`` configuration directory can be found in their `official documentaion <https://ipython.readthedocs.io/en/stable/config/intro.html#the-ipython-directory>`_.

#. Create directories to simulate the machine status at the beamline

   #. At your terminal, create simulation directories

      .. code-block:: none

         mkdir -v ~/acqsim
         mkdir -v ~/acqsim/xpdUser
         mkdir -v ~/acqsim/xpdConfig

   #. Create an empty long-term beamline config file

      .. code-block:: none

         echo '{}' >~/acqsim/xpdConfig/XPD_beamline_config.yml

#. Enter ``ipython`` with ``collection`` profile specified from your terminal. This is command is essentially the same as ``bsui`` you will be typing at beamline!

   .. code-block:: none

      ipython --profile=collection

#. You should be prompted into an ``ipython`` session, simulating your upcoming beamline experience. Please refer to the `quikstart guide in xpdAcq documentation <https://xpdacq.github.io/xpdAcq/quickstart.html>`_ to run your simulated beamline and enjoy playing!

   * You may find yourself need a syntax to create your simulated beamtime object and get everything running. This quick code snippet may be helpful for you.

      .. code-block:: python

         bt = _start_beamtime('simulation', saf_num=300000, experimenters=['Jane', 'Doe'], wavelength=0.184649)
