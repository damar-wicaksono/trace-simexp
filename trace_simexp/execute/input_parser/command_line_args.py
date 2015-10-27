"""Module to parse command line input arguments - Execute phase
"""

__author__ = "Damar Wicaksono"


def get():
    r"""Get the command line arguments of the execute phase

    :return:
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="trace_simexp Execute - Run all preprocessed trace inputs"
    )

    # The fullname of info_file from the pre-processing phase
    parser.add_argument(
        "-info", "--info_file",
        type=str,
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

    # Get the command line arguments
    args = parser.parse_args()

    return args.info_file, args.num_processors, args.scratch_directory, \
           args.trace_executable, args.xtv2dmx_executable


def check(inputs):
    r"""Check the validity of the inputs

    :return:
    """