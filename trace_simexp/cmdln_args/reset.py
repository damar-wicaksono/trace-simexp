# -*- coding: utf-8 -*-
"""
    trace_simexp.cmdln_args.reset
    *****************************

    Module to parse command line arguments used for reset
"""
from .._version import __version__

__author__ = "Damar Wicaksono"


def get() -> list:
    """Get the command line arguments of the execute phase

    :return: list of string, the contents of an info file
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="%(prog)s - trace-simexp Reset: Return prior to a phase"
    )

    # The fullname of info_file from the pre-processing phase
    parser.add_argument(
        "-info", "--info_file",
        type=argparse.FileType("rt"),
        help="The info file of a phase",
        required=True
    )

    # Print the version
    parser.add_argument(
        "-V", "--version",
        action="version",
        version="%(prog)s (trace-simexp version {})" .format(__version__)
    )

    # Get the command line arguments
    args = parser.parse_args()

    # Read file argument contents
    with args.info_file as info_file:
        info_file_contents = info_file.read().splitlines()

    return info_file_contents
