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


    # Sample has to be specified
    # Select individual samples
    if args.num_samples is not None:
        # Sample number has to be positive
        if True in [_ < 0 for _ in args.num_samples]:
            parser.error(
                "Number of samples with -ns has to be strictly positive!")
        else:
             return args.num_samples, args.info_file, args.num_processors, \
                    args.scratch_directory, args.trace_executable, \
                    args.xtv2dmx_executable

    # Use range of samples
    elif args.num_range is not None:
        # Sample range number has to be positive
        if (args.num_range[0] <= 0 or args.num_range[1] <= 0) and \
                (args.num_range[0] > args.num_range[1]):
            parser.error("Sample range with -nr has to be strictly positive!"
                         "and the first is smaller than the second")
        else:
            samples = list(range(args.num_range[0], args.num_range[1]+1))
            return samples, args.info_file, args.num_processors, \
                   args.scratch_directory, args.trace_executable, \
                   args.xtv2dmx_executable

    # Select all samples
    elif args.all_samples is not None:
        return args.all_samples, args.info_file, args.num_processors, \
               args.scratch_directory, args.trace_executable, \
               args.xtv2dmx_executable


def check(inputs):
    r"""Check the validity of the inputs

    :return:
    """