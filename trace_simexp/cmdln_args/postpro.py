"""Module to parse command line arguments in post-processing phase
"""

__author__ = "Damar Wicaksono"


def get():
    """Get the command line arguments of the postpro phase

    :return: (str) the exec.info file, fullname
        (str) the list of TRACE variables file, fullname
        (str) the aptplot executable, fullname if not in the path
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="trace_simexp postpro - Postprocess the TRACE xtv/dmx"
    )

    # The fullname of info_file from the
    parser.add_argument(
        "-exec", "--exec_info",
        type=str,
        help="The execution phase info file",
        required=True
    )

    # The list of trace variables to be extraced
    parser.add_argument(
        "-vars", "--trace_variables",
        type=str,
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

    # Get the command line arguments
    args = parser.parse_args()

    return args.exec_info, args.trace_variables, args.aptplot_executable, \
        args.num_processors