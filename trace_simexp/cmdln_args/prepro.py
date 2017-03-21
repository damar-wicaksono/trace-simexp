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

    :return: tuple of the following values:
        (int or string) the specified samples, individual, range, or all
        (str) the base directory name of the simulation campaign
        (str) the base tracin fullname
        (str) the design matrix fullname
        (str) the list of parameters fullname
        (bool) the flag whether to overwrite directory structure
        (str) the oneline info of the simulation experiment campaign
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="%(prog)s - trace-simexp, Preprocess: Generate TRACE inputs"
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

    # The base directory name
    parser.add_argument(
        "-b", "--base_name",
        type=str,
        help="The base directory name",
        default="./simulation",
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
        help="Ovewrite existing directory structures",
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
    tracin_base_fullname = args.base_tracin.name
    with args.base_tracin as tracin:
        tracin_base_contents = tracin.read().splitlines()
    design_matrix_fullname = args.design_matrix.name
    with args.design_matrix as dm_file:
        design_matrix_contents = util.parse_csv(dm_file)
    params_list_fullname = args.params_list.name
    with args.params_list as params_file:
        params_list_contents = params_file.read().splitlines()

    # Sample has to be specified, check the way it was specified
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

    return samples, args.base_name, \
           tracin_base_fullname, tracin_base_contents, \
           design_matrix_fullname, design_matrix_contents, \
	   params_list_fullname, params_list_contents, \
	   args.overwrite, args.info, args.prepro_filename


def check(inputs):
    r"""Check the validity of the command line arguments

    :param inputs: (dict) the command line arguments as dictionary
    :return: ValueError if exception raised
    """
    import os
    import numpy as np

    # Get the number 
    num_samples = inputs["dm_contents"].shape[0]
    num_params_dm = inputs["dm_contents"].shape[1]

    # Check the number of parameters listed in the params_list_file
    num_params_list_file = 0
    for i in inputs["params_list_contents"]:
        if not i.startswith("#"):
            num_params_list_file += 1

    # Check the number of parameters in the dm file and list of parameters file
    if num_params_list_file != num_params_dm:
        raise ValueError("The number of parameters is inconsistent\n"
                         "{:10d} in {} and {:10d} in {}"
                         .format(num_params_list_file,
                                 inputs["params_list_name"],
                                 num_params_dm,
                                 inputs["dm_name"]))
    else:
        pass

    # Check if the sample number asked is available
    if not isinstance(inputs["samples"], bool):
        if max(inputs["samples"]) > num_samples:
            raise ValueError("The sample asked is beyond the available "
                             "samples\n {:10d} asked and {:10d} in {}"
                         .format(max(inputs["samples"]),
                                 num_samples,
                                 inputs["dm_name"]))
    else:
        pass

