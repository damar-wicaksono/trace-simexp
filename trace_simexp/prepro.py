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


def read_params(param_list_file: str,
                info_filename: str,
                comment_char: str="#") -> dict:
    """Read list of parameters file and create a python dictionary out of it

    :param param_list_file: (str) the fullname of list of parameters file
    :param info_filename: (str) the filename string for info_file
    :param comment_char: (str) the character signifying comment line in the file
    :returns: (list of dict) the parameter perturbation specification in a list
        of dictionary
    """
    from .paramfile import common
    from .paramfile import senscoef
    from .paramfile import matprop
    from .paramfile import spacer
    from .paramfile import comp

    # the list of supported component type
    COMPONENTS = ["pipe", "vessel", "power", "fill", "break"]

    # the list of dictionary of parameters list
    params_dict = list()

    # Open and read list of parameters file
    with open(param_list_file, "rt") as params_file:
        for line in params_file.readlines():
            if not line.startswith(comment_char):
                line = line.strip()
                # the keyword for data type is the second entry in each line
                keyword = line.split()[1].lower()

                if keyword == "spacer":
                    # spacer grid data is specified, update params_dict
                    params_dict.append(spacer.parse(line))

                elif keyword == "matprop":
                    # material properties data is specified, update params_dict
                    params_dict.append(matprop.parse(line))

                elif keyword == "senscoef":
                    # sensitivity coefficient is specified, update params_dict
                    params_dict.append(senscoef.parse(line))

                elif keyword in COMPONENTS:
                    # component parameter is specified, update params_dict
                    params_dict.append(comp.parse(line))

                else:
                    raise NameError("*{}* data type is not supported!"
                                    .format(keyword))

    # Append the prepro.info
    common.append_info(params_dict, info_filename)

    return params_dict


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
