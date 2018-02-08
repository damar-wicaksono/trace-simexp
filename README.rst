trace-simexp
============

A python module with utilities to assist in carrying out simulation experiment 
with TRACE code.

The general flow chart of the processes involved in ``trace_simexp`` package is

.. image:: ./docs/figures/flowchart.png

Features
--------

 - Complete separation of the processes in 3 different steps: **prepro**, 
   **exec**, and **postpro**.
 - Three modes of parameter perturbation are supported: additive, 
   multiplicative, and substitutive
 - Four categories of TRACE variables in the input deck can be perturbed:
   spacer grid, material properties, *sensitivity coefficient*, and components
 - For TRACE components, five are supported: PIPE, VESSEL, POWER, FILL, BREAK
 - Specification of the computer experiment by the users is done throug a set 
   of input files (list of parameters file, design matrix file, and list of 
   graphic variables)
 - Iso-probabilistic transformation of the normalized design matrix is 
   available for uniform, discrete, and log-uniform

Complete log of changes can be found in `CHANGELOG`_.

.. _CHANGELOG: ./CHANGELOG.md

Requirements
------------

The module was developed and tested using the `Anaconda Python`_ distribution
of Python v3.5.
No additional package except the base installation of the distribution is required.

.. _Anaconda Python: https://www.continuum.io/downloads

Installation
------------

``trace-simexp`` is hosted on `GitHub`_.

.. _GitHub: https://github.com/damar-wicaksono/trace-simexp

after cloning the source::

    git clone git@github.com:damar-wicaksono/trace-simexp.git

the installation can be done easily from the local source directory::

    pip install -e .

This will make the following available in the path:

 - The python module ``trace_simexp``
 - ``trace_simexp_prepro`` executable
 - ``trace_simexp_execute`` executable
 - ``trace_simexp_postpro`` executable
 - ``trace_simexp_reset`` executable

Further Documentation
---------------------

Documentation of ``trace-simexp`` is an on-going process.
The current version can be found in the ``/docs`` folder and
can be built with the following ``make`` command (given that ``sphinx`` has been
installed)::

    make html

to build the html version of the documentation.
Note that the html documentation used ``rtd`` theme which can be installed via ``pip``::

    pip install sphinx-rtd-theme

The index file can then be found in::

    ./docs/build/html/index.html

Currently, a bare minimum set of documentations is available for ``trace-simexp``.
The user's guide can be found in the *Usage* section while the contributor's 
guide can be found in the *Implementation* section.
The latest version of the documentation is hosted on `readthedocs`_.

.. _readthedocs: http://trace-simexp.readthedocs.io/en/latest/index.html

License
-------

The project is licensed under the MIT License.
