# -*- coding: utf-8 -*-
"""
    trace_simexp.cmdln_args.postpro
    *******************************
    
    Module to parse command line arguments used in the post-processing phase
"""
from .._version import __version__

__author__ = "Damar Wicaksono"


def get():
    """Get the command line arguments of the post-pro phase
    
    :return: a tuple with the following contents
        (str) the exec.nfo file, fullname
        (list) the contents of the exec.nfo 
        (str) the list of TRACE variables file, fullname
        (list) the contents of the list of TRACE variables file
        (str) the aptplot executable, fullname if not in the path
        (int) the number of processors used
        (bool/list) if not specified samples return True, otherwise
            it is a list of samples to be post-processed
        (str) the postpro info filename if specified, otherwise the 
            current working directory
    """
    import argparse
    from . import common

    parser = argparse.ArgumentParser(
        description="%(prog)s - Postpro: Postprocess the TRACE dmx"
    )

    # The fullname of info_file from the execution phase
    parser.add_argument(
        "-exec", "--exec_file",
        type=argparse.FileType("rt"),
        help="The execution phase info file",
        required=True
    )

    # The list of trace variables to be extracted
    parser.add_argument(
        "-vars", "--xtv_variables",
        type=argparse.FileType("rt"),
        help="The list of TRACE variables file",
        required=True
    )

    # The aptplot executable
    parser.add_argument(
        "-aptplot", "--aptplot_executable",
        type=str,
        help="The aptplot executable",
        required=True
    )

    # The number of processors
    parser.add_argument(
        "-nprocs", "--num_processors",
        type=int,
        help="The number of available processors",
        default=1,
        required=False
    )

    # Select which samples to run
    parser.add_argument(
        "-ns", "--num_samples",
        type=int,
        nargs="+",
        help="Select samples to run",
        required=False
    )

    # Select a range of samples to run
    parser.add_argument(
        "-nr", "--num_range",
        type=int,
        nargs=2,
        help="Range of samples to run, between two values, inclusive",
        required=False
    )

    # Select all of the available samples
    parser.add_argument(
        "-as", "--all_samples",
        action="store_true",
        help="Execute all samples in prepro info file (default)",
        default=False,
        required=False
    )

    # The overwrite flag
    parser.add_argument(
        "-ow", "--overwrite",
        action="store_true",
        help="Reset existing select run directories",
        default=False,
        required=False
    )

    # The info filename
    parser.add_argument(
        "-postpro_info", "--postpro_filename",
        type=str,
        help="The post-process info filename "
             "(by default, will be created in the current working directory)",
        required=False,
        default=None
    )

    # Print version
    parser.add_argument(
        "-V", "--version",
        action="version",
        version="%(prog)s (trace-simexp version {})" .format(__version__)
    )

    # Get the command line arguments
    args = parser.parse_args()

    # Check if any sample is specified and each are mutually exclusive
    common.check_samples_argument(args.num_samples,
                                  args.num_range,
                                  args.all_samples)

    # Read the contents of the execute phase info file
    exec_info_fullname, exec_info_contents = \
        common.get_fullname_and_contents(args.exec_file)
    # Read the contents of the list of TRACE graphic variables file
    xtv_vars_fullname, xtv_vars_contents = \
        common.get_fullname_and_contents(args.xtv_variables)

    # Check and get the executable for APTPLOT
    aptplot_executable = common.get_executable(args.aptplot_executable)

    # Check the validity of the number of processors
    if args.num_processors <= 0:
        raise ValueError("The number of processors must be > 0")

    # Sample does not have to be explicitly specified, by default all will be
    # post-processed.
    # Select individual samples
    if args.num_samples is not None:
        samples = args.num_samples
    elif args.num_range is not None:
        samples = list(range(args.num_range[0], args.num_range[1]+1))
    else:
        # By default post-process all samples
        samples = True

    # Execute phase info filename, expand to absolute path
    postpro_filename = common.expand_path(args.postpro_filename)

    return (exec_info_fullname, exec_info_contents,
            xtv_vars_fullname, xtv_vars_contents,
            aptplot_executable, args.num_processors,
            samples, args.overwrite, postpro_filename)
