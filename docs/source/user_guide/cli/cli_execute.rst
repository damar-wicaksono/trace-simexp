.. _trace_simexp_execute:

Execute (``trace_simexp_execute``)
==================================

In the execute step, all the input decks that were created in the pre-processing
step are executed sequentially in batch.
This means that the script will traverse the run directories created before and
execute TRACE using the input deck inside sequentially.
The size of a batch is controlled by the number of processors supplied by the
user through the command line argument.

``trace_simexp_execute`` is the driver script to carry out the execute step.
It can be invoked in the terminal using the following command::

    trace_simexp_execute -prepro <the preprocessing step info file> \
                         -nprocs <the number of available processors> \
                         -{ns, nr, as} <selection of samples to be executed> \
                         -scratch <the scratch directory> \
                         -trace <the trace executable> \
                         -xtv2dmx <the xtv2dmx executable>

Brief explanation on the required arguments can be printed on the screen
using the following command::

    trace_simexp_execute --help

The table below gives the complete options/flags in detail.

=== ========== ==================== ========== ======== ================================================= =========
No. Short Name Long Name            Type       Required Description                                       Default
=== ========== ==================== ========== ======== ================================================= =========
1   -h         --help               flag       No       Show help message and exit                        None
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
12  -V         --version            flag       No       Show the program's version number and exit        None
=== ========== ==================== ========== ======== ================================================= =========

The script execution will also produce an info file (from here on
in will be called *exec info file*). The info file is produced by default
with the following naming convention::

    exec-<tracin name>-<parlist name>-<dm name>-<sample_start>_<sample_end>-<YYMMDD>-<HHMMSS>.nfo

The file is used to document the command line arguments specified when the
script was called, to log the process run for diagnostic purpose, as well as be
used in the subsequent (post-processing) step.
See below for the example of the contents.

Simultaneous execution of multiple TRACE simulation often requires large amount
of disk space even for a single case.
To save disk space, the utility takes two measures.
First, the binary ``xtv`` file is not written directly in the running
directory during the execution.
Instead a soft link is created inside the running directory, linked to the
actual ``xtv`` file written in a *scratch* directory.
This approach was adopted to limit the disk space usage in a STARS project
working directory (or *the activity folder*) that is a backup volume and
limited to 200 [GB] currently.
The so-called *scratch* directory usually resides in a non-backup volume.
This measure is optional and is applied when ``-scratch`` option is provided
with a valid directory. Otherwise, the ``xtv`` will be written directly in
the run directory.

Second, after each execution, the resulting `xtv` file will be directly
converted to the more space efficient *dmx* format. This is done by using
`xtv2dmx` utility. As such, the path to the scratch directory as well as the
path to the executable for `xtv2dmx` utility are needed to be supplied during
the call.
This option is always active and at this point cannot be override.

Example
-------

Following the previous example, executing the following command will
execute all of the TRACE input decks created in the previous step using 5
processors (or, parallel jobs with multiple batches each of size 5)::

    python execute.py -prepro prepro-febaTrans214-febaVars2Params-optLHS_110_2-1_110.info \
                      -scratch /afs/psi.ch/group/lrs/scratch/grp.lrs.scr001.nb/wicaksono_d/ \
                      -trace trace_v5.0p3.uq_extended \
                      -xtv2dmx xtv2dmx_v6.5.2_inst01.sh \
                      -nprocs 5 >& 214_1060_7.log &

**Remarks**: The utility was so far tested in the ``lclrs`` machines. To keep the
kerberos token active for a long session, it is advised to use the ``k5run -B``
command and put the job in the background with the following command instead::

    k5run -B python execute.py -prepro prepro-febaTrans214-febaVars2Params-optLHS_110_2-1_110.info \
                               -scratch /afs/psi.ch/group/lrs/scratch/grp.lrs.scr001.nb/wicaksono_d/ \
                               -trace trace_v5.0p3.uq_extended \
                               -xtv2dmx xtv2dmx_v6.5.2_inst01.sh \
                               -nprocs 5 >& 214_1060_7.log &

Based on the command above, the prepro info file will be created with the
following name::

    exec-febaTrans214-febaVars2Params-optLHS_110_2-1_110-<160327>-<002107>.nfo

The file has the following (abridged with the ellipsis) contents::

    TRACE Simulation Experiment - Date: 2016-03-27 00:26:06.547934
    ***Execute Phase Info***
    prepro.info Filename          -> prepro-febaTrans214-febaVars2Params-optLHS_110_2-1_110.info
    TRACE Executable              -> trace_v5.0p3.uq_extended
    XTV2DMX Executable            -> xtv2dmx_v6.5.2_inst01.sh
    Scratch Directory Name        -> /afs/psi.ch/group/lrs/scratch/grp.lrs.scr001.nb/wicaksono_d
    Number of Processors          -> 5  (lclrs73)
    Samples to Run                ->
      1      2      3      4      5      6      7      8      9     10
     11     12     13     14     15     16     17     18     19     20
    ...
    101    102    103    104    105    106    107    108    109    110
    *** Batch Execution -     1 ***
    Execution Successfull: trace_v5.0p3.uq_extended -p febaTrans214-run_1
    Execution Successfull: trace_v5.0p3.uq_extended -p febaTrans214-run_3
    Execution Successfull: trace_v5.0p3.uq_extended -p febaTrans214-run_5
    Execution Successfull: trace_v5.0p3.uq_extended -p febaTrans214-run_2
    Execution Successfull: trace_v5.0p3.uq_extended -p febaTrans214-run_4
    Execution Successfull: xtv2dmx_v6.5.2_inst01.sh -r febaTrans214-run_1.xtv -d febaTrans214-run_1.dmx
    Execution Successfull: xtv2dmx_v6.5.2_inst01.sh -r febaTrans214-run_3.xtv -d febaTrans214-run_3.dmx
    Execution Successfull: xtv2dmx_v6.5.2_inst01.sh -r febaTrans214-run_5.xtv -d febaTrans214-run_5.dmx
    Execution Successfull: xtv2dmx_v6.5.2_inst01.sh -r febaTrans214-run_2.xtv -d febaTrans214-run_2.dmx
    Execution Successfull: xtv2dmx_v6.5.2_inst01.sh -r febaTrans214-run_4.xtv -d febaTrans214-run_4.dmx
    ...
    *** Batch Execution -    22 ***
    Execution Successfull: trace_v5.0p3.uq_extended -p febaTrans214-run_106
    Execution Successfull: trace_v5.0p3.uq_extended -p febaTrans214-run_108
    Execution Successfull: trace_v5.0p3.uq_extended -p febaTrans214-run_110
    Execution Successfull: trace_v5.0p3.uq_extended -p febaTrans214-run_107
    Execution Successfull: trace_v5.0p3.uq_extended -p febaTrans214-run_109
    Execution Successfull: xtv2dmx_v6.5.2_inst01.sh -r febaTrans214-run_106.xtv -d febaTrans214-run_106.dmx
    Execution Successfull: xtv2dmx_v6.5.2_inst01.sh -r febaTrans214-run_108.xtv -d febaTrans214-run_108.dmx
    Execution Successfull: xtv2dmx_v6.5.2_inst01.sh -r febaTrans214-run_110.xtv -d febaTrans214-run_110.dmx
    Execution Successfull: xtv2dmx_v6.5.2_inst01.sh -r febaTrans214-run_107.xtv -d febaTrans214-run_107.dmx
    Execution Successfull: xtv2dmx_v6.5.2_inst01.sh -r febaTrans214-run_109.xtv -d febaTrans214-run_109.dmx
