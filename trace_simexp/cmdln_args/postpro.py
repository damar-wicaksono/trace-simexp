"""Module to parse command line arguments in post-processing phase
"""
from .. import util
from ..__init__ import __version__

__author__ = "Damar Wicaksono"


def get():
    """Get the command line arguments of the postpro phase

    :return: (str) the exec.info file, fullname
        (str) the list of TRACE variables file, fullname
        (str) the aptplot executable, fullname if not in the path
    """
    import os
    import argparse

    parser = argparse.ArgumentParser(
        description="%(prog)s - trace-simexp Postpro: Postprocess the TRACE dmx"
    )

    # The fullname of info_file from the execution phase
    parser.add_argument(
        "-exec", "--exec_file",
        type=argparse.FileType("rt"),
        help="The execution phase info file",
        required=True
    )

    # The fullname of info_file from the pre-processing phase
    parser.add_argument(
        "-prepro", "--prepro_file",
        type=argparse.FileType("rt"),
        help="The pre-processing phase info file",
        required=True
    )

    # The list of trace variables to be extraced
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

    # The info filename
    parser.add_argument(
        "-postpro", "--postpro_file",
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

    # Read the files content into list
    exec_info_fullname = args.exec_file.name
    with args.exec_file as exec_file:
        exec_info_contents = exec_file.read().splitlines()
    prepro_info_fullname = args.prepro_file.name
    with args.prepro_file as prepro_file:
        prepro_info_contents = prepro_file.read().splitlines()
    xtv_vars_fullname = args.xtv_variables.name
    with args.xtv_variables as xtv_vars_file:
        xtv_vars_contents = xtv_vars_file.read().splitlines()

    # Check if the executable for aptplot exist and valid
    if len(args.aptplot_executable.split("/")) > 1:
        # Given full path of AptPlot exec
        if not os.path.isfile(args.aptplot_executable):
            raise ValueError("The specified AptPlot executable not found!")
    else:
        # Assumed Aptplot exec in path
        if not util.cmd_exists(args.aptplot_executable):
            raise ValueError("The specified AptPlot executable not found!")

    # Check the validity of the number of processors
    if args.num_processors <= 0:
        raise ValueError("The number of processors must be > 0")

    return exec_info_fullname, exec_info_contents, \
           prepro_info_fullname, prepro_info_contents, \
           xtv_vars_fullname, xtv_vars_contents, \
           args.aptplot_executable, args.num_processors, args.postpro_file
