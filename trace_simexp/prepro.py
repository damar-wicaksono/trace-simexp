"""Main module for pre-processing activities - Pre-processing Phase
"""

__author__ = "Damar Wicaksono"


def get_input(info_filename: str=None) -> dict:
    """Get all the inputs for pre-processing phase

    Sources of inputs are: command line arguments, list of parameters file,
    trace base input, and design matrix file

    :param info_filename: the string of prepro.info file
    :return: All the inputs required for pre-processing phase in a dictionary
    """
    r"""Get the command line arguments and construct a dictionary from it

    :param info_filename: (str, optional) the filename for the info_file, it
        will be constructed based on input arguments if nothing is specified
    :return: (dict) the command line arguments collected
    """
    import numpy as np
    from . import cmdln_args
    from . import info_file

    # Read the command line arguments
    samples, base_dirname, \
        tracin_base_fullname, dm_fullname, params_list_fullname, \
        overwrite, info = cmdln_args.prepro.get()

    base_name = base_dirname.split("/")[-1]
    case_name = tracin_base_fullname.split("/")[-1].split(".")[0]
    dm_name = dm_fullname.split("/")[-1].split(".")[0]
    params_list_name = params_list_fullname.split("/")[-1].split(".")[0]

    # Read the list of parameters file

    # Make a template string

    # Read the design matrix

    # Construct the dictionary
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
    cmdln_args.prepro.check(inputs)

    # Update samples if all samples are asked
    if isinstance(inputs["samples"], bool) and inputs["samples"]:
        num_samples = np.loadtxt(inputs["dm_file"]).shape[0]
        inputs["samples"] = list(range(1, num_samples+1))

    # Write to a file the summary of pre-processing
    if info_filename is not None:
        info_file.prepro.write(inputs, info_filename)
        inputs["info_file"] = info_filename
    else:
        info_filename = info_file.common.make_filename(inputs, "prepro")
        info_file.prepro.write(inputs, info_filename)
        inputs["info_file"] = info_filename

    return inputs


def create_dirtree(prepro_inputs: dict):
    """Create a directory structure for the simulation campaign

    :param prepro_inputs: All the inputs required for pre-pro in a dictionary
    """
    return None


def reset(postpro_inputs: dict):
    """Delete the created directory structures according to the parameters

    :param prepro_inputs: (dict) the input parameters for pre-processing phase
    """
    return None
