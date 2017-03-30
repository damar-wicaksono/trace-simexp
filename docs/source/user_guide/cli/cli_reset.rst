.. _trace_simexp_reset:

Reset Phase (``trace_simexp_reset``)
====================================

``trace_simexp_reset`` allows the user to reset a completed phase into its original state.
It can be invoked from the terminal using the following command::

    trace_simexp_reset -info <info file fullname>

Brief explanation on the required arguments can be printed on the screen using the following command::

    trace_simexp_reset --help

The table below lists the complete options/flag in detail.

=== ============= ==================== ========== ======== ========================================== =======
No. Short Name    Long Name            Type       Required Description                                Default
=== ============= ==================== ========== ======== ========================================== =======
1   -h            --help               flag       No       Show the help message and exit             None
2   -info         --info_file          string     Yes      A completed phase info file (path+name)    None
3   -V            --version            flag       No       Show the program's version number and exit False
=== ============= ==================== ========== ======== ========================================== =======

The return to original state depends on the info file being passed:

1. postpro: delete all the resulting ``csv`` files produced
   from the post-processing phase listed in the info file
2. execute: delete all files, except the TRACE input file, inside the run directories
   listed in execute phase info file
3. prepro: delete all files and run-directories of the produced
   by pre-processing phase as listed the phase info file

The user will be prompted one more chance to review and confirm what's going to be purged in the reset phase.

.. warning::
    There would be no turning back after confirming that the specified files or directories are to be purged.
    Review the listed files carefully.

Example
-------

Resetting the previous post-processing phase can be done using the following command::

    trace_simexp_reset -info postpro-febaTrans216-feba216Vars27-lhs_200_27-1_5-xtvVars-170328-125447.nfo

after which the user will be prompted with the following question::

    /afs/psi.ch/project/stars/workspace/RND/SB-RND-ACT-006-13/WD41/projects/trace-simexp/febaTrans216/feba216Vars27-lhs_200_27/febaTrans216-run_1-xtvVars.csv will be deleted.
    /afs/psi.ch/project/stars/workspace/RND/SB-RND-ACT-006-13/WD41/projects/trace-simexp/febaTrans216/feba216Vars27-lhs_200_27/febaTrans216-run_3-xtvVars.csv will be deleted.
    /afs/psi.ch/project/stars/workspace/RND/SB-RND-ACT-006-13/WD41/projects/trace-simexp/febaTrans216/feba216Vars27-lhs_200_27/febaTrans216-run_5-xtvVars.csv will be deleted.
    Delete all CSV files? [y/N]

Press ``y`` to confirm purging.

Resetting the previous execute phase back to before its completion can be done similarly::

    trace_simexp_reset -info exec-febaTrans216-feba216Vars27-lhs_200_27-1_5-170328-122617.nfo

After which the prompt would be::

    /afs/psi.ch/project/stars/workspace/RND/SB-RND-ACT-006-13/WD41/projects/trace-simexp/febaTrans216/feba216Vars27-lhs_200_27/febaTrans216-run_1 will be revert back to pre-pro state!
    /afs/psi.ch/project/stars/workspace/RND/SB-RND-ACT-006-13/WD41/projects/trace-simexp/febaTrans216/feba216Vars27-lhs_200_27/febaTrans216-run_3 will be revert back to pre-pro state!
    /afs/psi.ch/project/stars/workspace/RND/SB-RND-ACT-006-13/WD41/projects/trace-simexp/febaTrans216/feba216Vars27-lhs_200_27/febaTrans216-run_5 will be revert back to pre-pro state!
    Revert select directories to pre-process state? Warning: this will delete all except *.inp file. [y/N]

Finally, to reset everything back to prior to pre-processing phase (basically purge everything), use the command::

    trace_simexp_reset -info prepro-febaTrans216-feba216Vars27-lhs_200_27-1_5-170328-120237.nfo

The prompt after executing this command would be::

    /afs/psi.ch/project/stars/workspace/RND/SB-RND-ACT-006-13/WD41/projects/trace-simexp/febaTrans216/feba216Vars27-lhs_200_27/febaTrans216-run_1 will be deleted!
    /afs/psi.ch/project/stars/workspace/RND/SB-RND-ACT-006-13/WD41/projects/trace-simexp/febaTrans216/feba216Vars27-lhs_200_27/febaTrans216-run_3 will be deleted!
    /afs/psi.ch/project/stars/workspace/RND/SB-RND-ACT-006-13/WD41/projects/trace-simexp/febaTrans216/feba216Vars27-lhs_200_27/febaTrans216-run_5 will be deleted!
    Delete the select run directories? (Warning: this will delete them all) [y/N] y
