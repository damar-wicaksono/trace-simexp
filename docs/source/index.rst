.. trace-simexp documentation master file, created by
   sphinx-quickstart on Tue Sep 20 19:09:35 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

``trace-simexp`` Package
========================

A computer experiment is a multiple model runs using different values of the
model parameters. Its design, in particular the selection of the design points
at which the model will be evaluated; as well as its analysis, in particular the
analysis of the output variation in relation to the inputs variation, are
useful for sensitivity and uncertainty analyses of the model subjected to the
experimentation.

An important prerequisite of carrying out such experiment is the availability
of a supporting tool able to handle the related logistical aspects. A
Python3-based scripting utility has been developed to assist in carrying such
experiments for thermal-hydraulics system code TRACE.The scope of the utility is
ranging from the pre-processing of the TRACE input deck amenable for batch
parallel execution to the post-treatment of the resulting binary xtv/dmx file
amenable to subsequent sensitivity and uncertainty analyses. This documentation
describes the development of the tool, including the description of its usage,
implementations, and assumptions.

trace-simexp Documentation
==========================

.. toctree::
  :maxdepth: 2

  basics
  user_guide
  implementation
  developer_guide
  about

trace-simexp Modules reference documentation
============================================

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
