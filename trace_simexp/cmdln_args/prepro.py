# -*- coding: utf-8 -*-
"""
    trace_simexp.cmdln_args.prepro
    ******************************

    Module to parse command line arguments used in the pre-processing step
"""
from .._version import __version__

__author__ = "Damar Wicaksono"


def get() -> tuple:
    r"""Parse input arguments required for pre-processing phase

    :return: tuple with the following values:
        (int or string) the specified samples, individual, range, or all
        (str) the base directory name of the simulation campaign
        (str) the base TRACE input deck fullname (path + filename)
        (str) the design matrix fullname (path + filename)
        (str) the list of parameters fullname (path + filename)
        (bool) the flag whether to overwrite directory structure
        (str) a one line info of the simulation experiment campaign
    """
    import argparse
    from . import common

    parser = argparse.ArgumentParser(
        description="%(prog)s - Preprocess: Generate TRACE perturbed inputs"
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
        help="Process all samples in design matrix (default)",
        default=False,
        required=False
    )

    # The base directory name
    parser.add_argument(
        "-b", "--base_dirname",
        type=str,
        help="The base directory name (Default: current working directory)",
        default="./",
        required=False
    )

    # The base tracin filename
    parser.add_argument(
        "-tracin", "--base_tracin",
        type=argparse.FileType("rt"),
        help="The base tracin filename",
        required=True
    )

    # The base design matrix filename
    parser.add_argument(
        "-dm", "--design_matrix",
        type=argparse.FileType("rt"),
        help="The design matrix filename",
        required=True
    )

    # The list of parameter filename
    parser.add_argument(
        "-parlist", "--params_list",
        type=argparse.FileType("rt"),
        help="The list of parameters filename",
        required=True
    )

    # The overwrite flag
    parser.add_argument(
        "-ow", "--overwrite",
        action="store_true",
        help="Overwrite existing directory structures",
        default=False,
        required=False
    )

    # The tag message
    parser.add_argument(
        "-info", "--info",
        type=str,
        help="The tag message",
        required=False
    )

    # The info filename
    parser.add_argument(
        "-prepro_info", "--prepro_filename",
        type=str,
        help="The pre-process info filename "
             "(by default, will be created in the current working directory)",
        required=False,
        default=None
    )

    # Print version
    parser.add_argument(
        "-V", "--version",
        action="version",
        version="%(prog)s (trace-simexp version {})".format(__version__)
    )

    # Get the command line arguments
    args = parser.parse_args()

    # Check if any sample is specified and each are mutually exclusive
    common.check_samples_argument(args.num_samples,
                                  args.num_range,
                                  args.all_samples)

    # Read Base TRACE input deck
    tracin_base_fullname, tracin_base_contents = \
        common.get_fullname_and_contents(args.base_tracin)
    # Read Design matrix file
    design_matrix_fullname, design_matrix_contents = \
        common.get_fullname_and_contents(args.design_matrix, dsv=True)
    # Read List of parameters file
    params_list_fullname, params_list_contents = \
        common.get_fullname_and_contents(args.params_list)

    # Available samples from the design matrix
    num_samples = design_matrix_contents.shape[0]
    num_dimension = design_matrix_contents.shape[1]
    avail_samples = list(range(1, num_samples + 1))

    # Sample has to be specified, otherwise all available in the design matrix
    # will be processed. Check the way it was specified and get them
    # Select individual samples
    if args.num_samples is not None:
        samples = common.get_samples(args.num_samples, avail_samples)
    # Use range of samples
    elif args.num_range is not None:
        samples = list(range(args.num_range[0], args.num_range[1]+1))
        samples = common.get_samples(samples, avail_samples)
    # Select all samples, by default
    else:
        samples = avail_samples

    # Check the validity of the design matrix dimension and list of params file
    check_dimension(params_list_contents, num_dimension)

    # Base Directory Name, most probably supplied in a relative path
    base_dirname = common.expand_path(args.base_dirname)

    # Prepro phase info filename, expand to absolute path
    prepro_filename = common.expand_path(args.prepro_filename)

    return (samples, base_dirname,
            tracin_base_fullname, tracin_base_contents,
            design_matrix_fullname, design_matrix_contents,
            params_list_fullname, params_list_contents,
            args.overwrite, args.info, prepro_filename)


def check_dimension(params_list_contents: list, num_dimension: int):
    r"""Check the validity of the list of parameters file size

    :param params_list_contents: the contents of the file
    :param num_dimension: the dimension of the design matrix file
    """
    # Check the number of parameters listed in the params_list_file
    num_params = 0
    for line in params_list_contents:
        if not line.startswith("#"):
            num_params += 1

    # Check the number of parameters in the dm file and list of parameters file
    if num_params != num_dimension:
        raise ValueError("The number of parameters is inconsistent\n"
                         "{:5d} in list of parameters file and {:5d} in "
                         "the design matrix file"
                         .format(num_params, num_dimension))
    else:
        pass
