__author__ = "Damar Wicaksono"


def get(info_filename=None):
    r"""Get the command line arguments and construct a dictionary from it

    :param info_filename: (str, optional) the filename for the info_file, it
        will be constructed based on input arguments if nothing is specified
    :return: (dict) the command line arguments collected
    """
    import numpy as np
    from .input_parser import command_line_args
    from .input_parser import info_file

    inputs = dict()

    samples, base_dirname, tracin_base_fullname, \
    dm_fullname, params_list_fullname, overwrite, info = command_line_args.get()

    base_name = base_dirname.split("/")[-1]
    case_name = tracin_base_fullname.split("/")[-1].split(".")[0]
    dm_name = dm_fullname.split("/")[-1].split(".")[0]
    params_list_name = params_list_fullname.split("/")[-1].split(".")[0]

    inputs = {
        "samples": samples,
        "base_dir": base_dirname,
        "base_name": base_name,
        "tracin_base_file": tracin_base_fullname,
        "case_name": case_name,
        "dm_file": dm_fullname,
        "dm_name": dm_name,
        "params_list_file": params_list_fullname,
        "params_list_name": params_list_name,
        "overwrite": overwrite,
        "info": info
    }

    # Check the validity of the inputs
    command_line_args.check(inputs)

    # Update samples if all samples are asked
    if isinstance(inputs["samples"], bool) and inputs["samples"]:
        num_samples = np.loadtxt(inputs["dm_file"]).shape[0]
        inputs["samples"] = list(range(1, num_samples+1))

    # Write to a file the report summary
    if info_filename is not None:
        info_file.write(inputs, info_filename)
        inputs["info_file"] = info_filename
    else:
        info_filename = info_file.make_filename(inputs)
        info_file.write(inputs, info_filename)
        inputs["info_file"] = info_filename

    return inputs





