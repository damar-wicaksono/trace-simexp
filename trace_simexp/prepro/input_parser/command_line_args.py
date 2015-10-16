"""Module to parse command line input arguments
"""

__author__ = "Damar Wicaksono"


def get():
    r"""Parse input arguments required for preprocessing phase

    :return:
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="trace_simexp Preprocessor - Create tracin and dirtree"
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
        type=str,
        help="The base tracin filename",
        required=True
    )

    # The base design matrix filename
    parser.add_argument(
        "-dm", "--design_matrix",
        type=str,
        help="The design matrix filename",
        required=True
    )

    # The list of parameter filename
    parser.add_argument(
        "-parlist", "--params_list",
        type=str,
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

    # Get the command line arguments
    args = parser.parse_args()

    # Check if any sample is specified
    if args.num_samples is None and args.num_range is None:
        parser.error("either -ns or -nr has to be present!")
    elif args.num_samples is not None and args.num_range is not None:
        parser.error("-ns or -nr cannot both be present!")

    if args.num_samples is not None:
        return args.num_samples, args.base_name, args.base_tracin,\
               args.design_matrix, args.params_list, args.overwrite
    elif args.num_range is not None:
        samples = list(range(args.num_range[0], args.num_range[1]+1))
        return samples, args.base_name, args.base_tracin,\
               args.design_matrix, args.params_list, args.overwrite
