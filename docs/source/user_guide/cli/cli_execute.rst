.. _trace_simexp_execute:

Execute (``trace_simexp_execute``)
==================================

In the execute step,
all the input decks that were created in the pre-processing step are executed sequentially in batch.
This means that the script will traverse the run directories created before and
execute TRACE using the input deck inside sequentially.
The size of a batch is controlled by the number of processors supplied by
the user through the command line argument.

``trace_simexp_execute`` is the driver script to carry out the execute step.
It can be invoked in the terminal using the following command::

    trace_simexp_execute -prepro <the preprocessing step info file> \
                         -nprocs <the number of available processors> \
                         -{ns, nr, as} <selection of samples to be executed> \
                         -scratch <the scratch directory> \
                         -trace <the trace executable> \
                         -xtv2dmx <the xtv2dmx executable>

Brief explanation on the required arguments can be printed on the screen using the following command::

    trace_simexp_execute --help

The table below gives the complete options/flags in detail.

=== ========== ==================== ========== ======== ================================================= =========
No. Short Name Long Name            Type       Required Description                                       Default
=== ========== ==================== ========== ======== ================================================= =========
1   -h         --help               flag       No       Show help message and exit                        False
2   -prepro    --prepro_info        string     Yes      The prepro info file (path+name)                  None
3   -nprocs    --num_processors     integer    No       The number of processors (batch process size)     1
4   -ns        --num_samples        integer(s) No       Execute select samples                            None
5   -nr        --num_range          2 integers No       Execute samples between these values, inclusive   None
6   -as        --all_samples        flag       No       Execute all samples available in prepro info file True
7   -scratch   --scratch_directory  string     No       Path to scratch directory                         See below
8   -trace     --trace_executable   string     Yes      The TRACE executable, in PATH or specified        None
9   -xtv2dmx   --xtv2dmx_executable string     Yes      The XTV2DMX executable, in PATH or specified      None
10  -ow        --overwrite          flag       No       Flag to overwrite existing directory              None
11  -exec_info --exec_filename      string     No       The execute phase info filename                   See below
12  -V         --version            flag       No       Show the program's version number and exit        False
=== ========== ==================== ========== ======== ================================================= =========

The script execution will also produce an info file (from here on in will be called *exec info file*).
The info file is produced by default with the following naming convention::

    exec-<tracin_name>-<parlist_name>-<dm_name>-<sample_start>_<sample_end>-<YYMMDD>-<HHMMSS>.nfo

The file is used to document the command line arguments specified when the script was called,
to log the process run for diagnostic purpose, as well as
be used in the subsequent (post-processing) step.
See below for the example of the contents.

Simultaneous execution of multiple TRACE simulation often requires large amount of disk space even for a single case.
To save disk space, the utility takes two measures.
First, the binary ``xtv`` file is not written directly in the running directory during the execution.
Instead a soft link is created inside the running directory,
linked to the actual ``xtv`` file written in a *scratch* directory.
This approach was adopted to limit the disk space usage in a STARS project working directory (or *the activity folder*)
that is a backup volume and limited to 200 [GB] currently.
The so-called *scratch* directory usually resides in a non-backup volume.
This measure is optional and is applied when ``-scratch`` option is provided with a valid directory.
Otherwise, the ``xtv`` will be written directly in the run directory.

Second, after each execution, the resulting `xtv` file will be directly converted to the more space efficient *dmx* format.
This is done by using `xtv2dmx` utility.
As such, the path to the scratch directory as well as
the path to the executable for `xtv2dmx` utility are needed to be supplied during the call.
This option is always active and at this point cannot be override.

Example
-------

Following the previous example, executing the following command will
execute all of the TRACE input decks created in the previous step::

    trace_simexp_execute -prepro ./nfo/prepro-febaTrans216-feba216Vars27-lhs_200_27-1_5-170328-120237.nfo \
                         -xtv2dmx xtv2dmx_v6.5.2_inst01.sh \
                         -trace trace_v5.0p3.uq_extended \
                         -exec_info ./nfo

By default, if not specified, all samples available in the prepro info file will be executed.
Also by default, the dmx file will be produced inside each respective run directory if a scratch directory is not specified.
Finally, by default the execution will be carried out sequentially in batch of size 1 (the number of processors).

.. note::

    The utility was so far tested in the one of the ``lclrs`` machines.
    To keep the ``kerberos`` token active for a long session,
    it is advised to use the ``k5run -B`` command and put the job in the background
    with the following command instead::

        k5run -B    trace_simexp_execute -prepro ./nfo/prepro-febaTrans216-feba216Vars27-lhs_200_27-1_5-170328-120237.nfo \
                                         -xtv2dmx xtv2dmx_v6.5.2_inst01.sh \
                                         -trace trace_v5.0p3.uq_extended \
                                         -exec_info ./nfo >& 216_3_27.log &

    the ``216_3_27.log`` file is an arbitrary file to redirect standard output
    and standard error.

Based on the command above, the prepro info file will be created with the following name::

   exec-febaTrans216-feba216Vars27-lhs_200_27-1_5-170328-122617.nfo

The file has the following (abridged with the ellipsis) contents::

    TRACE Simulation Experiment - Date: 2017-03-28 12:26:17.939115
    ***Execute Phase Info***
    prepro.info Name              -> prepro-febaTrans216-feba216Vars27-lhs_200_27-1_5-170328-120237.nfo
    prepro.info File              -> /afs/psi.ch/project/stars/workspace/RND/SB-RND-ACT-006-13/WD41/projects/trace-simexp/nfo/prepro-febaTrans2
    Base Directory Name           -> /afs/psi.ch/project/stars/workspace/RND/SB-RND-ACT-006-13/WD41/projects/trace-simexp
    Base Case Name                -> febaTrans216
    List of Parameters Name       -> feba216Vars27
    Design Matrix Name            -> lhs_200_27
    TRACE Executable              -> trace_v5.0p3.uq_extended
    XTV2DMX Executable            -> xtv2dmx_v6.5.2_inst01.sh
    Number of Processors          -> 1  (lclrs71)
    Samples to Run                ->
        1      3      5
    ***  End of Samples  ***
    *** Batch Execution -     1 ***
    Execution Successful: trace_v5.0p3.uq_extended -p febaTrans216-run_1
    Execution Successful: xtv2dmx_v6.5.2_inst01.sh -r febaTrans216-run_1.xtv -d febaTrans216-run_1.dmx
    *** Batch Execution -     2 ***
    Execution Successful: trace_v5.0p3.uq_extended -p febaTrans216-run_3
    Execution Successful: xtv2dmx_v6.5.2_inst01.sh -r febaTrans216-run_3.xtv -d febaTrans216-run_3.dmx
    *** Batch Execution -     3 ***
    Execution Successful: trace_v5.0p3.uq_extended -p febaTrans216-run_5
    Execution Successful: xtv2dmx_v6.5.2_inst01.sh -r febaTrans216-run_5.xtv -d febaTrans216-run_5.dmx

