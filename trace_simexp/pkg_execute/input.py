"""Module to get command line input parameters for the execute phase
"""

__author__ = "Damar Wicaksono"


def get(info_filename=None):
    """Get the command line arguments, read the info file, and construct dict()

    :return: (dict) the inputs collected as dictionary
    """
    from .input_parser import command_line_args
    from .input_parser import info_file

    inputs = dict()

    # Read the command line arguments
    samples, info_fullname, num_procs, scratch_dir, trace_exec, xtv2dmx_exec = \
        command_line_args.get()

    # Get the info filename, exclude the path
    info_name = info_fullname.split("/")[-1]

    # Read the pre-processing phase info file
    base_dir, case_name, params_list_name, dm_name, avail_samples = \
        info_file.prepro_read(info_fullname)

    # Check if samples is within the available samples
    if isinstance(samples, bool) and samples:
        samples = avail_samples
    elif set(samples) < set(avail_samples):
        samples = samples
    else:
        raise ValueError("Requested samples is not part of the available ones")

    # Get the name of the machine (hostname)
    hostname = command_line_args.get_hostname()

    # Construct the dictionary
    inputs = {
        "info_name": info_file,
        "info_file": info_fullname,
        "num_procs": num_procs,
        "scratch_dir": scratch_dir,
        "trace_exec": trace_exec,
        "xtv2dmx_exec": xtv2dmx_exec,
        "base_dir": base_dir,
        "case_name": case_name,
        "params_list_name": params_list_name,
        "dm_name": dm_name,
        "samples": samples,
        "hostname": hostname
    }

    # todo: Check the validity of the inputs

    # Write to a file the summary of execution phase parameters
    if info_filename is not None:
        info_file.write(inputs, info_filename)
        inputs["exec_info"] = info_filename
    else:
        info_filename = info_file.make_filename(inputs)
        info_file.write(inputs, info_filename)
        inputs["exec_info"] = info_filename

    return inputs