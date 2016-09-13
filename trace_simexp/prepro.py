"""Main module for pre-processing activities - Pre-processing Phase
"""
import numpy as np


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
    from . import util

    # Read the command line arguments
    samples, base_dirname, \
        tracin_base_file, dm_file, params_list_file, \
        overwrite, info = cmdln_args.prepro.get()
    
    # Get the names of directory and files
    base_name = base_dirname.split("/")[-1]
    case_name = tracin_base_file.name.split("/")[-1].split(".")[0]
    dm_name = dm_file.name.split("/")[-1].split(".")[0]
    params_list_name = params_list_file.name.split("/")[-1].split(".")[0]

    # Construct the dictionary
    inputs = {
        "samples": samples,
        "base_dir": base_dirname,
        "base_name": base_name,
        "tracin_base_file": tracin_base_file,
        "tracin_base_fullname": tracin_base_file.name,
        "case_name": case_name,
        "dm_file": dm_file,
        "dm_fullname": dm_file.name,
        "dm_name": dm_name,
        "params_list_file": params_list_file,
        "params_list_fullname": params_list_file.name,
        "params_list_name": params_list_name,
        "overwrite": overwrite,
        "info": info
    }

    # Check the validity of the inputs
    cmdln_args.prepro.check(inputs)

    # Update samples if all samples are asked
    if isinstance(inputs["samples"], bool) and inputs["samples"]:
        num_samples = util.parse_csv(inputs["dm_file"]).shape[0]
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


def read_params(params_list_file,
                info_filename: str,
                tracin_filename:str,
                comment_char: str="#") -> dict:
    """Read list of parameters file and create a python dictionary out of it

    The nominal parameter values are read from the base tracin file

    :param param_list_file: (file) list of parameters file
    :param info_filename: (str) the filename string for info_file
    :param tracin_filename: (str) the filename string for base tracin file
    :param comment_char: (str) the character signifying comment line in the file
    :returns: (list of dict) the parameter perturbation specification in a list
        of dictionary
    """
    from .paramfile import common
    from .paramfile import senscoef
    from .paramfile import matprop
    from .paramfile import spacer
    from .paramfile import comp
    from . import tracin

    # Reset file back to the first line
    params_list_file.seek(0)

    # the list of supported component type
    COMPONENTS = ["pipe", "vessel", "power", "fill", "break"]

    # the list of dictionary of parameters list
    params_dict = list()

    # Open and read list of parameters file
    #with open(param_list_file, "rt") as params_file:
    for line in params_list_file.readlines():
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

    # Get the nominal values of parameter from tracin and update params_dict
    tracin.get_nominal_values(tracin_filename, params_dict)

    return params_dict


def create_dirtree(prepro_inputs: dict,
                   params_dict: dict,
                   tracin_template: str,
                   dm_array: np.ndarray):
    """Create a directory structure for the simulation campaign

    :param params_dict: (list of dict) the list of parameters
    :param str_template: (str template) the template based on base tracin
    :param dm: (ndArray) the numpy array
    :param case_name: (str) the name of the case
    :param params_list_name: (str) the name of the list of parameters file
    :param dm_name: (str) the name of the design matrix
    :param samples: (list) the list of samples to be created
    :return:
    """
    import os
    from . import tracin

    # Put the dictionary into corresponding local variables
    # The name of the case
    case_name = prepro_inputs["case_name"]
    # the name of the list of parameters file
    params_list_name = prepro_inputs["params_list_name"]
    # the name of the design matrix file
    dm_name = prepro_inputs["dm_name"]
    # the samples
    samples = prepro_inputs["samples"]
    # the base name
    base_name = prepro_inputs["base_name"]
    # the overwrite directive
    overwrite = prepro_inputs["overwrite"]

    # Create directory path name
    case_name_dir = "./{}/{}" .format(base_name, case_name)
    dm_name_dir = "{}/{}-{}" .format(case_name_dir, params_list_name, dm_name)

    if not os.path.exists(dm_name_dir):
        os.makedirs(dm_name_dir)

    # Loop over required samples
    for i in samples:
        num_runs = i
        run_dir_name = "{}/{}-run_{}" .format(dm_name_dir, case_name, num_runs)

        if not os.path.exists(run_dir_name):
            os.makedirs(run_dir_name)

        str_tracin = tracin.create(tracin_template,
                                   params_dict,
                                   dm_array[i-1, :])
        tracin_filename = "{}-run_{}.inp" .format(case_name, num_runs)
        tracin_fullname = "{}/{}" .format(run_dir_name, tracin_filename)

        if os.path.isfile(tracin_fullname):
            if overwrite:
                with open(tracin_fullname, "wt") as tracin_file:
                    tracin_file.write(str_tracin)
            else:
                print("{} exist - no overwrite option" .format(tracin_fullname))
        else:
            with open(tracin_fullname, "wt") as tracin_file:
                    tracin_file.write(str_tracin)


def reset(prepro_inputs: dict):
    """Delete the created directory structures according to the parameters

    :param prepro_inputs: (dict) the input parameters for pre-processing phase
    """
    return None


def check_dirtree(case_name, param_list_name, dm_name, base_name, samples):
    """

    :param case_name:
    :param dm_name:
    :param samples:
    :return:
    """
    import os

    # Create directory path name
    case_name_dir = "./{}/{}" .format(base_name, case_name)
    dm_name_dir = "{}/{}" .format(case_name_dir, dm_name)

    print("********************************")
    print("Checking Directory Structures...")
    print("********************************")

    if os.path.exists(dm_name_dir):
        print("Simulation Case directory: {} exists"
              .format(dm_name_dir))
        print("\n")
    else:
        print("Simulation Case directory: {} does not exist"
              .format(dm_name_dir))
        print("\n")

    print("************************")
    print("Checking input files...")

    for i in samples:
        num_runs = i
        run_dir_name = "{}/{}_run_{}" .format(dm_name_dir, case_name, num_runs)

        if os.path.exists(run_dir_name):

            print("*********")
            print("Case Name - {} Design Matrix - {}.inp"
                  .format(case_name, dm_name))

            tracin_filename = "{}_run_{}.inp" .format(case_name, num_runs)
            tracin_fullname = "{}/{}" .format(run_dir_name, tracin_filename)

            if os.path.isfile(tracin_fullname):
                print("Sample - {}. Full path - {}" .format(num_runs,
                                                            tracin_fullname))
