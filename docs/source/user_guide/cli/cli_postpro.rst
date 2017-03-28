.. _trace_simexp_postpro:

Post-process (``trace_simexp_postpro``)
=======================================

After all the requested TRACE input decks (or samples) have been executed,
the resulting ``xtv`` files can be post-processed to extract the relevant variables
and put them into separate ``csv`` files,
placed inside the respective running directory.
The ``csv`` files, being text files, can be easily processed further with other tools for various purposes.
Similar to the execute step before,
the utility will traversed each of the executed running directory
and process the ``xtv`` file inside using the ``aptplot`` program to extract the requested variables.
The script also supports batch parallel execution.

``trace_simexp_postpro`` is the driver script to carry out the post-processing step.
It can be invoked in the terminal using the following command::

    trace_simexp_postpro -exec <the execute phase info file> \
                         -vars <the list of TRACE graphic variables file> \
                         -aptplot <the aptplot executable> \
                         -nprocs <the number of available processors> \
                         {-as, -ns, -nr} <argument to select samples to create, optional>

Brief explanation on the required arguments can be printed on the screen using the following command::

    trace_simexp_postpro --help

The table below lists the complete options/flag in detail.

=== ============= ==================== ========== ======== ============================================== =========
No. Short Name    Long Name            Type       Required Description                                    Default
=== ============= ==================== ========== ======== ============================================== =========
1   -h            --help               flag       No       Show the help message and exit                 None
2   -exec         --exec_info          string     Yes      The prepro info file (path+name)               None
3   -vars         --xtv_variables      string     Yes      The list of TRACE graphic variables            None
4   -aptplot      --aptplot_executable string     Yes      The APTPLOT executable, in PATH or specified   None
5   -nprocs       --num_processors     integer    No       The number of processors (batch process size)  1
6   -ns           --num_samples        integer(s) No       Pre-process the select of samples              None
7   -nr           --num_range          2 integers No       Post-process the range of samples, inclusive   None
8   -as           --all_samples        flag       No       Post-process all samples from exec.info        True
9   -ow           --overwrite          flag       No       Flag to overwrite the existing ``csv`` files   False
10  -postpro_info --postpro_filename   string     No       The post-process info filename                 See below
11  -V            --version            flag       No       Show the program's version number and exit     False
=== ============= ==================== ========== ======== ============================================== =========

.. note::
    When running the script interactively under Windows which is connected to an `lclrs` machine,
    the `aptplot` program requires that an X Server running in the background (e.g., `Xming`).

.. note::
    Make sure there is enough disk space in the running directory as the csv files being produced.
    Depending on how many variables are being extracted, the files (being a text file) can take considerable amount of disk space.
    Running out of space will break the postprocessing operations.
    At this point, no graceful exit nor warning are provided.

In addition to the postprocessing of the ``xtv`` files, the execution of postpro script will also produced an info file (hereinafter *postpro info file*).
The info file is produced by default with the following naming convention::

    postpro-<tracin_name>-<parlist_name>-<dm_name>-<sample_start>-_<sample_end>-<vars_name>-<YYMMDD>-<HHMMSS>.info

The file is used to document the command line arguments specified when the script was called as well as to log all the shell commands run during the execution.
See below for example of the contents.

**Example**

Following the previous example,
executing the following command will post-processed all of the TRACE ``dmx`` files produced in the previous step
using to extract TRACE graphic variables listed in the ``./simulation/xtvVars.apt`` file::

    trace_simexp_postpro -exec exec-febaTrans216-feba216Vars27-lhs_200_27-1_5-170328-122617.nfo \
                         -vars ./simulation/xtvVars.inp \
                         -aptplot aptplot_v6.5.2_inst01.sh \
                         -postpro_info ./nfo

By default, the execution is carried out using 1 processor and
all the availables samples listed in the exec info file will be post-processed.

.. note::
    Similar to the execute phase, if the postprocess step is expected to take a long time,
    it is advised that the job is sent to the background with ``k5run -B`` utility
    as given in the previous example.

Based on the command above, the prepro info file will be created with the following name::

    postpro-febaTrans216-feba216Vars27-lhs_200_27-1_5-xtvVars-170328-125447.nfo

The file has the following (abridged) contents::

    TRACE Simulation Experiment - Date: 2017-03-28 12:54:47.506218
    ***Post-process Phase Info***
    exec.info Name                -> exec-febaTrans216-feba216Vars27-lhs_200_27-1_5-170328-122617.nfo
    exec.info File                -> /afs/psi.ch/project/stars/workspace/RND/SB-RND-ACT-006-13/WD41/projects/trace-simexp/nfo/exec-febaTrans216
    Base Directory Name           -> /afs/psi.ch/project/stars/workspace/RND/SB-RND-ACT-006-13/WD41/projects/trace-simexp
    Base Case Name                -> febaTrans216
    List of Parameters Name       -> feba216Vars27
    Design Matrix Name            -> lhs_200_27
    APTPlot Executable            -> aptplot_v6.5.2_inst01.sh
    Number of Processors (Host)   -> 1  (lclrs71)
    List of XTV Variables Name    -> xtvVars
    List of XTV Variables File    -> /afs/psi.ch/project/stars/workspace/RND/SB-RND-ACT-006-13/WD41/projects/trace-simexp/simulation/xtvVars.in
    List of XTV Variables         ->
            rftn-20A69R29         rftn-20A89R29        rftn-20A109R29              pn-30A04         pn-1A17R01T01         pn-1A13R01T01
    Samples to Post-processed     ->
         1      3      5
    ***  End of Samples  ***
    *** Batch Execution -     1 ***
    Execution Successful: aptplot_v6.5.2_inst01.sh -batch febaTrans216-run_1-xtvVars.apt -nowin
    *** Batch Execution -     2 ***
    Execution Successful: aptplot_v6.5.2_inst01.sh -batch febaTrans216-run_3-xtvVars.apt -nowin
    *** Batch Execution -     3 ***
    Execution Successful: aptplot_v6.5.2_inst01.sh -batch febaTrans216-run_5-xtvVars.apt -nowin
