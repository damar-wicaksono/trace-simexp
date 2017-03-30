# -*- coding: utf-8 -*-
"""
    trace_simexp.prepro
    *******************

    Main module for pre-processing activities
"""

__author__ = "Damar Wicaksono"


def get_input() -> dict:
    """Get all the inputs for pre-processing phase

    Sources of inputs are: command line arguments, list of parameters file,
    trace base input, and design matrix file

    :return: All the inputs required for pre-processing phase in a dictionary

    +----------------------+--------------------------------------------------+
    | Key                  | Value                                            |
    +======================+==================================================+
    | samples              | (list, int > 0) The samples to be pre-processed, |
    |                      | a list of integer greater than zero              |
    +----------------------+--------------------------------------------------+
    | base_dirname         | (str) The full path base directory for set of    |
    |                      | input decks to be generated and subsequently     |
    |                      | executed                                         |
    +----------------------+--------------------------------------------------+
    | base_name            | (str) The base run directory name, taken from the|
    |                      | full path of the base directory)                 |
    +----------------------+--------------------------------------------------+
    | tracin_base_contents | (list, str) The contents of the base TRACE input |
    |                      | deck, line by line                               |
    +----------------------+--------------------------------------------------+
    | tracin_base_fullname | (str) The fullname of the base TRACE input deck  |
    +----------------------+--------------------------------------------------+
    | case_name            | (str) The case name is taken as the base TRACE   |
    |                      | input deck filename excluding the extension and  |
    |                      | the path                                         |
    +----------------------+--------------------------------------------------+
    | dm_contents          | (np.ndarray, float) The contents of the design   |
    |                      | matrix file as a numpy array                     |
    +----------------------+--------------------------------------------------+
    | dm_fullname          | (str) The fullname of the design matrix file     |
    +----------------------+--------------------------------------------------+
    | dm_name              | (str) The name of the design matrix file taken   |
    |                      | from the filename excluding the extension and    |
    |                      | the path                                         |
    +----------------------+--------------------------------------------------+
    | params_list_contents | (list, str) The contents of the the list of      |
    |                      | parameters file as a list of string              |
    +----------------------+--------------------------------------------------+
    | params_list_fullname | (str) The fullname of the list of parameters file|
    +----------------------+--------------------------------------------------+
    | params_list_name     | (str) The name of the list of parameters file,   |
    |                      | taken from the filename excluding the extension  |
    |                      | and the path                                     |
    +----------------------+--------------------------------------------------+
    | overwrite            | (bool) The flag to continue the pre-processing   |
    |                      | step even though info files and directory        |
    |                      | structures already exist                         |
    +----------------------+--------------------------------------------------+
    | info                 | (str) A short message for the simulation         |
    |                      | experiment                                       |
    +----------------------+--------------------------------------------------+
    | info_file            | (str) The filename of the preprocessing step info|
    +----------------------+--------------------------------------------------+
    """
    import os
    from . import cmdln_args
    from . import util
    from .info_file import common

    # Read the command line arguments
    samples, base_dirname, \
        tracin_base_fullname, tracin_base_contents, \
        dm_fullname, dm_contents, \
        params_list_fullname, params_list_contents, \
        overwrite, info, prepro_filename = cmdln_args.prepro.get()
    
    # Get the names of directory and files
    base_name = util.get_name(base_dirname)
    case_name = util.get_name(tracin_base_fullname)
    dm_name = util.get_name(dm_fullname)
    params_list_name = util.get_name(params_list_fullname)

    # Construct the dictionary
    inputs = {
        "samples": samples,
        "base_dirname": base_dirname,
        "base_name": base_name,
        "tracin_base_contents": tracin_base_contents,
        "tracin_base_fullname": tracin_base_fullname,
        "case_name": case_name,
        "dm_contents": dm_contents,
        "dm_fullname": dm_fullname,
        "dm_name": dm_name,
        "params_list_contents": params_list_contents,
        "params_list_fullname": params_list_fullname,
        "params_list_name": params_list_name,
        "overwrite": overwrite,
        "info": info
    }

    # Create the filename for the info file of the prepro phase
    if os.path.isdir(prepro_filename):
        # Append the filename with the full path
        prepro_filename = os.path.join(prepro_filename,
                                       common.make_filename(inputs, "prepro"))
    # Add new entry to the dictionary
    inputs["info_file"] = prepro_filename

    return inputs


def read_params(params_list_contents: list,
                tracin_base_contents: list,
                comment_char: str="#") -> list:
    """Read list of parameters file and create a python dictionary out of it

    The nominal parameter values are read from the base tracin file

    :param params_list_contents: the contents of list of parameters file
    :param tracin_base_contents: the contents of the base TRACE input deck
    :param comment_char: the character signifying comment line in the file
    :returns: the parameter perturbation specification as a list of dictionary
    """
    from .paramfile import senscoef
    from .paramfile import matprop
    from .paramfile import spacer
    from .paramfile import comp
    from . import tracin

    # the list of supported component type
    COMPONENTS = ["pipe", "vessel", "power", "fill", "break"]

    # the list of dictionary of parameters list
    params_dict = list()

    # Loop over the list elements
    for line in params_list_contents:
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

    # Get the nominal values of parameter from tracin and update params_dict
    tracin.get_nominal_values(tracin_base_contents, params_dict)

    return params_dict


def create_dirtree(prepro_inputs: dict,
                   params_dict: dict,
                   tracin_template: str):
    """Create a directory structure for the simulation campaign

    :param prepro_inputs: the complete inputs of the prepro step
    :param params_dict: the list of perturbed parameters
    :param tracin_template: the TRACE template with keys to be substituted with
        actual values from the rescaled design matrix
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
    base_dirname = prepro_inputs["base_dirname"]
    # the overwrite directive
    overwrite = prepro_inputs["overwrite"]
    # the design matrix array
    dm_array = prepro_inputs["dm_contents"]

    # Create directory path name
    case_name_dir = "{}/{}" .format(base_dirname, case_name)
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
                print("{} exist - no overwrite flag" .format(tracin_fullname))
        else:
            with open(tracin_fullname, "wt") as tracin_file:
                    tracin_file.write(str_tracin)


def reset(reset_inputs: dict):
    """Conduct reset operation for pre-processing phase

    :param reset_inputs: the required inputs for reset
    """
    import os
    from .util import make_dirnames
    from .util import query_yes_no
    from .task import clean

    # Make the path
    case_path = os.path.join(reset_inputs["base_dir"],
                             reset_inputs["case_name"])
    parlist_dm = "{}-{}".format(reset_inputs["params_list_name"],
                                reset_inputs["dm_name"])
    full_path = os.path.join(case_path, parlist_dm)

    if os.path.exists(full_path):
        # Create the list of run directories
        run_dirnames = make_dirnames(reset_inputs["samples"],
                                     reset_inputs, False)

        for run_dirname in run_dirnames:
            if os.path.exists(run_dirname):
                print("{} will be deleted!" .format(run_dirname))
            else:
                print("{} does not exist!" .format(run_dirname))

        if query_yes_no("Delete the select run directories?"
                        " (Warning: this will delete them all)", default="no"):
            # Remove folders
            clean.rm_files(run_dirnames)

            # Remove parent directories if they are empty
            if not os.listdir(full_path):
                os.rmdir(full_path)

            if not os.listdir(case_path):
                os.rmdir(case_path)
        else:
            pass

    else:
        print("No specified directory is found. Abort...")
