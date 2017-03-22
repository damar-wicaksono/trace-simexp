"""Module to parse command line arguments in the execute phase
"""
from .. import util
from .._version import __version__

__author__ = "Damar Wicaksono"


def get():
    """Get the command line arguments of the execute phase

    :return: the samples to be run can be chosen individually, a range, or all
        available samples. If all the function will return a boolean, otherwise
        its a list of integer.
        (str) the pre-processing phase info file, fullname
        (int) the number of processors used
        (str) the scratch directory
        (str) the trace executable fullname, if not in the path
        (str) the xtv2dmx executable fullname, if not in the path
    """
    import os
    import argparse

    parser = argparse.ArgumentParser(
        description="%(prog)s - trace-simexp, Execute: Run all TRACE inputs"
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
        help="Samples to run",
        required=False
    )

    # Select a range of samples to run
    parser.add_argument(
        "-nr", "--num_range",
        type=int,
        nargs=2,
        help="Range of samples to run",
        required=False
    )

    # Select all of the available samples
    parser.add_argument(
        "-as", "--all_samples",
        action="store_true",
        help="Run all samples",
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
    if args.num_samples is None and args.num_range is None \
            and not args.all_samples:
        parser.error("Either -ns, -nr, or -as has to be present!")
    elif args.num_samples is not None and args.num_range is not None:
        parser.error("-ns or -nr cannot both be present!")
    elif args.num_samples is not None and args.all_samples:
        parser.error("-ns or -as cannot both be present!")
    elif args.num_range is not None and args.all_samples:
        parser.error("-nr or -as cannot both be present!")
    else:
        pass

    # Read file argument contents
    prepro_info_fullname = args.prepro_info.name
    with args.prepro_info as prepro_info:
        prepro_info_contents = prepro_info.read().splitlines()

    # Check if the executables exist
    if len(args.trace_executable.split("/")) > 1:
        # Given full path of TRACE exec
        if not os.path.isfile(args.trace_executable):
            raise ValueError("The specified TRACE executable not found!")
    else:
        # Assumed TRACE exec in path
        if not util.cmd_exists(args.trace_executable):
            raise ValueError("The specified TRACE executable not found!")
    if len(args.xtv2dmx_executable.split("/")) > 1:
        # Given full path of XTV2DMX exec
        if not os.path.isfile(args.xtv2dmx_executable):
            raise ValueError("The specified XTV2DMX executable not found!")
    else:
        # Assumed XTV2DMX exec in path
        if not util.cmd_exists(args.xtv2dmx_executable):
            raise ValueError("The specified XTV2DMX executable not found!")

    # Guard against possible user input of directory closed with "/"
    # Otherwise there would be an error for directory creation due to "//"
    if args.scratch_directory is not None:
        scratch_directory = args.scratch_directory.split("/")
        if scratch_directory[-1] == "":
            scratch_directory.pop()
        scratch_directory = "/".join(scratch_directory)
    else:
        scratch_directory = None

    # Sample has to be specified
    # Select individual samples
    if args.num_samples is not None:
        # Sample number has to be positive
        if True in [_ < 0 for _ in args.num_samples]:
            parser.error(
                "Number of samples with -ns has to be strictly positive!")
        else:
            samples = args.num_samples

    # Use range of samples
    elif args.num_range is not None:
        # Sample range number has to be positive
        if (args.num_range[0] <= 0 or args.num_range[1] <= 0) and \
                (args.num_range[0] > args.num_range[1]):
            parser.error("Sample range with -nr has to be strictly positive!"
                         "and the first is smaller than the second")
        else:
            samples = list(range(args.num_range[0], args.num_range[1]+1))

    # Select all samples
    elif args.all_samples is not None:
        samples = args.all_samples

    # Return all the command line arguments
    return samples, prepro_info_fullname, prepro_info_contents, \
           args.num_processors, scratch_directory, \
           args.trace_executable, args.xtv2dmx_executable, args.exec_filename
