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

    # Get the command line arguments
    args = parser.parse_args()

    # Post-process the sample numbers
    if args.num_samples is None and args.num_range is None:
        parser.error("either -ns or -nr has to be present!")

    return args.num_samples