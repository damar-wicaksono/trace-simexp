.. _trace_simexp_cli:

======================
Command Line Interface
======================

Introduction
============

``trace_simexp`` is controlled using command-line interface (CLI).
All user's interaction with ``trace_simexp`` is done through a set of 
executables (or *driver scripts*) which are made available to the user 
in the path upon successfull installation of the package. 
The driver scripts include:

 1. ``trace_simexp_prepro``: Used to create a set of perturbed TRACE input deck
    and a directory structure for execution
 2. ``trace_simexp_execute``: Used to execute, in batches (within batch 
    parallel execution is possible), the generated perturbed TRACE input decks
 3. ``trace_simexp_postpro``: Used to extract a select set of variables from 
    TRACE binary output file (the so-called ``xtv/dmx`` file) into a ``csv`` 
    file 
 4. ``trace_simexp_reset``: Used to reset a completed phase to its original 
    state
 5. ``trace_simexp_freeze``: Used to update all the relevant information on the 
    info files information from absolute path to relative path (useful archival
    purpose)

If you simply execute ``trace_simexp`` a welcome screen will be displayed 
showing all available executables and their usage.

Pre-process (``trace_simexp_prepro``)
=====================================

``trace_simexp_prepro`` In the preprocessing step, the base TRACE input deck is modified by changing
the parameter values of the parameters listed in the list of parameter files
according to the values listed in the design matrix file. A set of new
perturbed TRACE input decks will be created and put into separate directories.
In subsequent execute step, these directories will serve as the run
directories. 

The preprocessing step driver script can be invoked in the terminal using the 
following command::

    trace_simexp_prepro {-as, -ns, -nr} <argument to select samples to create> \
                        -b <the base run directory name> \
                        -tracin <the base TRACE input deck> \
                        -dm <the design matrix> \
                        -parlist <the list of parameters file> \
                        -info <The short description of the campaign> \
                        -ow <flag to overwrite existing directory structure>

Brief explanation on this parameter can be shown using the following command::

    trace_simexp_prepro --help

The table below lists all the options/flag in detail.

=== ========== =============== ========== ================================ =============================================== =======
No. Short Name Long Name       Type       Required                         Description                                     Default    
=== ========== =============== ========== ================================ =============================================== =======
1   -as        --all_sample    flag/bool  Yes, iff -nr or -ns not supplied Preprocess all samples in design matrix         False      
2   -ns        --num_samples   integer(s) Yes, iff -as or -nr not supllied Preprocess the selected samples                 None       
3   -nr        --num_range     2 integers Yes, iff -as or -ns not supplied Preprocess the range of samples, inclusive      None       
4   -b         --base_name     string     No                               The base directory to spawn run directories     ./
5   -tracin    --base_tracin   string     Yes                              The base TRACE input deck, path+filename        None        
6   -dm        --design_matrix string     Yes                              The design matrix, path+filename                None        
7   -parlist   --params_list   string     Yes                              The list of parameters file, path+filename      None        
8   -info      --info          string     No                               Short message of the experiment                 None        
9   -ow        --overwrite     flag       No                               Flag to overwrite existing directory structure  False       
=== ========== =============== ========== ================================ =============================================== =======


The directories created is nested in the following form::

    .
    |
    +---<the base run directory name>
    |   +---<tracin>
    |       +---<parlist-dm>
    |           +---<tracin-run_1>
    |                   <tracin>-run_1.inp
    |           +---<tracin-run_2>
    |                   <tracin>-run_2.inp
    |           +---<tracin-run_3>
    |                   <tracin>-run_3.inp
    |
    ...

In addition to the creation of the run directory structure and perturbed TRACE
input deck, the script execution will also produce an info file (from here on
in will be called *prepro info file*). The info file is produced by default
with the following naming convention::

    prepro-<tracin>-<parlist>-<dm>-<sample_start>_<sample_end>-<date>-<time>.info

The file is used to document the command line arguments specified when the
script was called. It will also be used in the subsequent step.

Example
-------

For example, upon executing the following command::

    trace_simexp_prepro -tracin ./simulation/base/febaTrans214.inp \
                        -dm ./simulation/dmfiles/optLHS_110_2.csv \
                        -parlist ./simulation/paramfiles/febaVars2Params.inp \
                        -info "FEBA Test No. 214, 110 Samples, 2 Parameters"

A set of directory will be created::

    .
    |
    +---simulation
    |   +---febaTrans214
    |       +---febaVars7Params-optLHS_110_2
    |           +---febaTrans214-run_1
    |                   febaTrans214-run_1.inp
    |           +---febaTrans214-run_2
    |                   febaTrans214-run_2.inp
    |           +---febaTrans214-run_2
    |                   febaTrans214-run_3.inp
    ...
    |           +---febaTrans214-run_110
    |                   febaTrans214-run_110.inp              

Based on the command above, the prepro info file will be created with the 
following name::

    prepro-febaTrans214-febaVars2Params-optLHS_110_2-1_110-<160327>-<002107>.info

The file has the following (abridged) contents::

    TRACE Simulation Experiment - Date: 2016-03-27 00:21:07.196979
    FEBA Test No. 214, 110 Samples, 2 Parameters
    ***Preprocessing Phase Info***
    Base Name                     -> simulation
    Base Directory Name           -> /afs/psi.ch/project/stars/workspace/RND/SB-RND-ACT-006-13/WD41/projects/trace-simexp
    Base Case Name                -> febaTrans214
    Base Case File                -> /afs/psi.ch/project/stars/workspace/RND/SB-RND-ACT-006-13/WD41/projects/trace-simexp/simulation/base/febaTrans214.inp
    List of Parameters Name       -> febaVars2Params
    List of Parameters File       -> /afs/psi.ch/project/stars/workspace/RND/SB-RND-ACT-006-13/WD41/projects/trace-simexp/simulation/paramfiles/febaVars2Params.inp
    Design Matrix Name            -> optLHS_110_2
    Design Matrix File            -> /afs/psi.ch/project/stars/workspace/RND/SB-RND-ACT-006-13/WD41/projects/trace-simexp/simulation/dmfiles/optLHS_110_2.csv
    Samples to Run                ->
    1      2      3      4      5      6      7      8      9     10
     ...
    101    102    103    104    105    106    107    108    109    110
    ***  End of Samples  ***
    *** 1***
    Sensitivity Coefficient with ID *1039* is specified
    Parameter type: scalar
    Parameter perturbation mode: 3 (multiplicative)
    Parameter distribution: logunif
    1st distribution parameter: 0.250
    2nd distribution parameter: 4.000
    *** 2***
    Sensitivity Coefficient with ID *1011* is specified
    Parameter type: scalar
    Parameter perturbation mode: 3 (multiplicative)
    Parameter distribution: logunif
    1st distribution parameter: 0.500
    2nd distribution parameter: 2.000

Execute (``trace_simexp_execute``)
==================================

Post-process (``trace_simexp_postpro``)
=======================================

Reset (``trace_simexp_reset``)
==============================

Freeze (``trace_simexp_freeze``)
================================
