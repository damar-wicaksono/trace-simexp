# -*- coding: utf-8 -*-
"""
    trace_simexp.cmdln_args.prepro
    ******************************

    Module to parse command line arguments used in the pre-processing step
"""
from .. import util
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
    import os

    parser = argparse.ArgumentParser(
        description="%(prog)s - trace-simexp Preprocess: Generate TRACE inputs"
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
    if args.num_samples is not None and args.num_range is not None \
            and args.all_samples:
        parser.error("Ambiguous, -ns, -nr, and -as cannot all be present!")
    elif args.num_samples is not None and args.num_range is not None:
        parser.error("Ambiguous, -ns or -nr cannot both be present!")
    elif args.num_samples is not None and args.all_samples:
        parser.error("Ambiguous, -ns or -as cannot both be present!")
    elif args.num_range is not None and args.all_samples:
        parser.error("Ambiguous, -nr or -as cannot both be present!")

    # Read files argument contents
    tracin_base_fullname = os.path.abspath(args.base_tracin.name)
    with args.base_tracin as tracin:
        tracin_base_contents = tracin.read().splitlines()
    design_matrix_fullname = os.path.abspath(args.design_matrix.name)
    with args.design_matrix as dm_file:
        design_matrix_contents = util.parse_csv(dm_file)
    params_list_fullname = os.path.abspath(args.params_list.name)
    with args.params_list as params_file:
        params_list_contents = params_file.read().splitlines()

    # Available samples from the design matrix
    num_samples = design_matrix_contents.shape[0]
    num_dimension = design_matrix_contents.shape[1]

    # Sample has to be specified, otherwise all available in the design matrix
    # will be processed. Check the way it was specified and get them
    # Select individual samples
    if args.num_samples is not None:
        samples = get_sample_from_select(args.num_samples, num_samples)
    # Use range of samples
    elif args.num_range is not None:
        samples = get_sample_from_range(args.num_range, num_samples)
    # Select all samples, by default
    else:
        samples = list(range(1, num_samples + 1))

    # Check the validity of the design matrix dimension and list of params file
    check_dimension(params_list_contents, num_dimension)

    # Base Directory Name, most probably supplied in a relative path
    if args.base_dirname is not None:
        base_dirname = os.path.abspath(args.base_dirname)
    else:
        base_dirname = os.getcwd()  # Expand the current work dir. as default

    # Prepro phase info filename, expand to absolute path
    if args.prepro_filename is not None:
        prepro_filename = os.path.abspath(args.prepro_filename)
    else:
        prepro_filename = os.getcwd()

    return (samples, base_dirname,
            tracin_base_fullname, tracin_base_contents,
            design_matrix_fullname, design_matrix_contents,
            params_list_fullname, params_list_contents,
            args.overwrite, args.info, prepro_filename)


def get_sample_from_range(ranges: list, num_samples: int) -> list:
    r"""Get while checking the validity of the requested sample range

    :param ranges: The range of selected samples
    :param num_samples: The list of all selected samples based on the range
    :return: The selected samples, verified
    """
    samples = list(range(ranges[0], ranges[1] + 1))
    all_samples = list(range(1, num_samples + 1))

    # Check the validity of the sample range
    if (ranges[0] <= 0 or ranges[1] <= 0) and (ranges[0] > ranges[1]):
        raise ValueError(
            "Sample range with -nr has to be strictly positive, "
            "with the first is smaller than the second!")
    elif False in [_ in all_samples for _ in samples]:
        raise ValueError(
            "Some or all selected samples within range are not in the design!")

    return samples


def get_sample_from_select(samples: list, num_samples: int) -> list:
    r"""Get while checking the validity of the requested samples

    :param samples: The selected samples
    :param num_samples: The number of available samples
    :return: The selected samples, verified
    """
    all_samples = list(range(1, num_samples + 1))

    # Sample number has to be positive
    if True in [_ < 0 for _ in samples]:
        raise ValueError(
            "Number of samples with -ns has to be strictly positive!")
    # Sample number has to be within the available sample
    elif False in [_ in all_samples for _ in samples]:
        raise ValueError(
            "Some or all selected samples are not available in the design")

    return samples


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
