# -*- coding: utf-8 -*-
"""
    trace_simexp.cmdln_args.execute
    *******************************

    Module to parse command line arguments used in the execute phase
"""
from .._version import __version__

__author__ = "Damar Wicaksono"


def get():
    """Get the command line arguments of the execute phase

    :return: tuple with the following values:
        the samples to be run can be chosen individually, a range, or all
        available samples. If all the function will return a boolean, otherwise
        its a list of integer.
        (str) the pre-processing phase info file, fullname
        (int) the number of processors used
        (str) the scratch directory
        (str) the trace executable fullname, if not in the path
        (str) the xtv2dmx executable fullname, if not in the path
    """
    import argparse
    from . import common

    parser = argparse.ArgumentParser(
        description="%(prog)s - Execute: Run all TRACE inputs"
    )

    # The fullname of info_file from the pre-processing phase
    parser.add_argument(
        "-prepro", "--prepro_info",
        type=argparse.FileType("rt"),
        help="The pre-processing phase info file",
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

    # The fullname of the scratch directory
    parser.add_argument(
        "-scratch", "--scratch_directory",
        type=str,
        help="The scratch directory",
        required=False
    )

    # The trace executable
    parser.add_argument(
        "-trace", "--trace_executable",
        type=str,
        help="The trace executable",
        required=True
    )

    # The xtv2dmx executable
    parser.add_argument(
        "-xtv2dmx", "--xtv2dmx_executable",
        type=str,
        help="The xtv2dmx executable",
        required=True
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
        "-exec_info", "--exec_filename",
        type=str,
        help="The execute info filename",
        required=False,
        default=None
    )

    # Print the version
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

    # Read Pre-processing phase info file 
    prepro_info_fullname, prepro_info_contents = \
        common.get_fullname_and_contents(args.prepro_info)

    # Check and get the executables, both TRACE and XTV2DMX
    trace_executable = common.get_executable(args.trace_executable)
    xtv2dmx_executable = common.get_executable(args.xtv2dmx_executable)

    # Expand scratch directory
    scratch_directory = common.expand_path(args.scratch_directory, None)

    # Sample has to be specified, otherwise all samples listed in the prepro
    # info file will be executed. Check the way it was specified and get them
    # Select individual samples.
    if args.num_samples is not None:
        samples = args.num_samples
    # Use range of samples
    elif args.num_range is not None:
        samples = list(range(args.num_range[0], args.num_range[1]+1))
    else:
        # By default all samples is True
        samples = True

    # Execute phase info filename, expand to absolute path
    exec_filename = common.expand_path(args.exec_filename)

    # Return all the command line arguments
    return (samples, prepro_info_fullname, prepro_info_contents,
            args.num_processors, scratch_directory,
            trace_executable, xtv2dmx_executable, args.overwrite,
            exec_filename)
