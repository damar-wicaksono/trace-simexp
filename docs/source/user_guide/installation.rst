.. _trace_simexp_install:

============
Installation
============

Obtaining and installing ``trace-simexp`` is simple.
First is to download the current version hosted in bitbucket_.
and install it to your machine locally.
``trace-simexp`` is written in python3 and can be installed using ``pip``::

    > git clone https://bitbucket.org/lrs-uq/trace-simexp
    > cd trace-simexp
    > pip install .

Verifying the installation can be done by invoking::

    > trace_simexp
    trace-simexp version 0.4.0
    Conduct simulation experiment for TRACE

    Please use the driver scripts for each of the desired phases:
        trace_simexp_prepro     pre-process and generate perturbed inputs
        trace_simexp_execute    execute the generated perturbed inputs
        trace_simexp_postpro    extract select variables from dmx
        trace_simexp_reset      return the original state of a given phase
        trace_simexp_freeze     freeze current state for archival
    Use <driver_script> --help to get the help for each

.. _bitbucket: https://bitbucket.org/lrs-uq/trace-simexp

If you want to modify the package on the fly without re-installing it everytime to check the effect
use the ``-e`` (editable mode) when invoking ``pip``::

    > pip install -e .