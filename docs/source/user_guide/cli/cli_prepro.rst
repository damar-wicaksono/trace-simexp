.. _trace_simexp_prepro:

Pre-process (``trace_simexp_prepro``)
=====================================

In the pre-processing phase, the base TRACE input deck is modified by changing
the parameter values of the parameters listed in the list of parameter files
according to the values listed in the design matrix file.
A set of new perturbed TRACE input decks will be created and put into
separate directories.
In subsequent execute step, these directories will serve as the run
directories.

``trace_simexp_prepro`` is the driver script to carry out the preprocessing
phase. It can be invoked in the terminal using the following command::

    trace_simexp_prepro {-as, -ns, -nr} <argument to select samples to create> \
                        -b <the base run directory name> \
                        -tracin <the base TRACE input deck> \
                        -dm <the design matrix> \
                        -parlist <the list of parameters file> \
                        -info <The short description of the campaign> \
                        -prepro_info <The prepro info filename, optional>
                        -ow <flag to overwrite existing directory structure>

Brief explanation on this parameter can be shown using the following command::

    trace_simexp_prepro --help

The table below lists the complete options/flag in detail.

=== ============ ================= ========== ======== ============================================== =========
No. Short Name   Long Name         Type       Required Description                                    Default
=== ============ ================= ========== ======== ============================================== =========
1   -h           --help            flag       No       Show help message                              False
2   -ns          --num_samples     integer(s) No       Pre-process the selected samples               None
3   -nr          --num_range       2 integers No       Pre-process the range of samples, inclusive    None
4   -as          --all_sample      flag/bool  No       Pre-process all samples in design matrix       True
5   -b           --base_dirname    string     No       The base directory to spawn run directories    ./
6   -tracin      --base_tracin     string     Yes      The base TRACE input deck, path+filename       None
7   -dm          --design_matrix   string     Yes      The design matrix, path+filename               None
8   -parlist     --params_list     string     Yes      The list of parameters file, path+filename     None
9   -info        --info            string     No       Short message of the experiment                None
10  -prepro_info --prepro_filename string     No       The pre-process info filename                  See below
11  -ow          --overwrite       flag       No       Flag to overwrite existing directory structure False
12  -V           --version         flag       No       Show the program's version number and exit     False
=== ============ ================= ========== ======== ============================================== =========

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

    prepro-<tracin_name>-<parlist_name>-<dm_name>-<sample_start>_<sample_end>-<YYMMDD>-<HHMMSS>.info

The file is used to document the command line arguments specified when the
script was called. It will also be used in the subsequent step.

Example
-------

For example, upon executing the following command::

    trace_simexp_prepro -ns 1 3 5 \
                        -tracin ./simulation/febaTrans216.inp \
                        -dm ./simulation/lhs_200_27.csv \
                        -parlist ./simulation/feba216Vars27.inp \
                        -info "FEBA Test No. 214, 110 samples (select 1,3,5), 27 Parameters" \
                        -prepro_info ./nfo

A set of directory will be created in the current working directory::

    .
    |
    +---febaTrans214
    |   +---febaVars7Params-optLHS_110_2
    |       +---febaTrans214-run_1
    |           febaTrans214-run_1.inp
    |       +---febaTrans214-run_2
    |           febaTrans214-run_2.inp
    |       +---febaTrans214-run_3
    |           febaTrans214-run_3.inp

Based on the command above, the prepro info file will be created with the
following name under the ``./nfo`` folders::

    prepro-febaTrans216-feba216Vars27-lhs_200_27-1_5-170328-120237.nfo.info

The file has the following (abridged) contents::

    TRACE Simulation Experiment - Date: 2017-03-28 12:02:37.678582
    FEBA Test No. 214, 110 samples (select 1,3,5), 27 Parameters
    ***Pre-process Phase Info***
    Base Name                     -> trace-simexp
    Base Directory Name           -> /afs/psi.ch/project/stars/workspace/RND/SB-RND-ACT-006-13/WD41/projects/trace-simexp
    Base Case Name                -> febaTrans216
    Base Case File                -> /afs/psi.ch/project/stars/workspace/RND/SB-RND-ACT-006-13/WD41/projects/trace-simexp/simulation/febaTrans216.inp
    List of Parameters Name       -> feba216Vars27
    List of Parameters File       -> /afs/psi.ch/project/stars/workspace/RND/SB-RND-ACT-006-13/WD41/projects/trace-simexp/simulation/feba216Vars27.inp
    Design Matrix Name            -> lhs_200_27
    Design Matrix File            -> /afs/psi.ch/project/stars/workspace/RND/SB-RND-ACT-006-13/WD41/projects/trace-simexp/simulation/lhs_200_27.csv
    Samples to Run                ->
         1      3      5
    ***  End of Samples  ***
    *** 1***
    Component *break* ID *40*, parameter *ptb* is specified
    Parameter type: table
    Parameter perturbation mode: 3 (multiplicative)
    Perturbation factor probability distribution:
    - distribution: *unif*
    - min: 0.9
    - max: 1.1
    *** 2***
    Component *fill* ID *10*, parameter *tltb* is specified
    Parameter type: table
    Parameter perturbation mode: 2 (additive)
    Perturbation factor probability distribution:
    - distribution: *unif*
    - min: -5.0
    - max: 5.0
    ...
    ***26***
    Sensitivity Coefficient with ID *1044* is specified
    Parameter type: scalar
    Parameter perturbation mode: 2 (additive)
    Perturbation factor probability distribution:
    - distribution: *unif*
    - min: -50.0
    - max: 50.0
    ***27***
    Spacer grid with Grid ID *1*, parameter *spmatid* is specified
    Parameter type: scalar
    Parameter perturbation mode: 1 (substitutive)
    Perturbation factor probability distribution:
    - distribution: *discrete*
    - 8: 0.25
    - 2: 0.1
    - 10: 0.15
    - 6: 0.5

