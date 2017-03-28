.. _trace_simexp_cli:

======================
Command Line Interface
======================

``trace_simexp`` is controlled using command-line interface (CLI),
all user's interaction with the functionalities provided by the package
is done through a set of executables (or *driver scripts*)
which are made available to the user in the path upon successful installation of the package.
The driver scripts include:

.. toctree::
   :maxdepth: 1

   cli/cli_prepro
   cli/cli_execute
   cli/cli_postpro
   cli/cli_reset
   cli/cli_freeze

Short description of each driver script is the following:

+---------------------------------------------------+-----------------------------------+
|Driver Script                                      |Short Description                  |
+===================================================+===================================+
|:ref:`trace_simexp_prepro <trace_simexp_prepro>`   | Used to create a set of perturbed |
|                                                   | TRACE input deck and a directory  |
|                                                   | structure for execution           |
+---------------------------------------------------+-----------------------------------+
|:ref:`trace_simexp_execute <trace_simexp_execute>` | Used to execute, in batches       |
|                                                   | (within batch parallel execution  |
|                                                   | is possible), the generated       |
|                                                   | perturbed TRACE input decks       |
+---------------------------------------------------+-----------------------------------+
|:ref:`trace_simexp_postpro <trace_simexp_postpro>` | Used to extract a                 |
|                                                   | select set of variables from TRACE|
|                                                   | binary output (the so-called      |
|                                                   | ``xtv/dmx`` file) into a ``csv``  |
+---------------------------------------------------+-----------------------------------+
|:ref:`trace_simexp_reset <trace_simexp_reset>`     | Used to reset a completed         |
|                                                   | phase to its original state       |
+---------------------------------------------------+-----------------------------------+
|:ref:`trace_simexp_freeze <trace_simexp_freeze>`   | Used to update all the            |
|                                                   | relevant information on the info  |
|                                                   | files information from absolute   |
|                                                   | path to relative path (archival)  |
+---------------------------------------------------+-----------------------------------+


If you simply execute ``trace_simexp`` a welcome screen will be displayed showing all available executables and their usage.
