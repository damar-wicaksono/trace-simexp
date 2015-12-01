"""Module to parse sensitivity coefficient data from the list of parameters file
"""

__author__ = "Damar Wicaksono"


def parse(line, params_dict, info_filename=None):
    r"""Parse sensitivity coefficient specification from list of parameters file

    note that the input argument `params_dict` is mutable and will be modified

    :param line: (list of str) a line read from list of parameters file
    :param params_dict: (list of dict) the list of parameters in a dictionary
    :param verbose: (bool) terminal printing or not
    :returns: (list of dict) an updated params_dict with senscoef specification
    """
    senscoef_data = line.split()

    senscoef_dict = {
        "enum": int(senscoef_data[0]),
        "data_type": "senscoef",
        "var_num": int(senscoef_data[2]),
        "var_name": None,
        "var_type": senscoef_data[4].lower(),
        "var_mode": int(senscoef_data[5]),
        "var_card": None,
        "var_word": None,
        "var_dist": senscoef_data[8].lower(),
        "var_par1": float(senscoef_data[9]),
        "var_par2": float(senscoef_data[10]),
        "str_fmt": senscoef_data[11]
    }

    # Check the validity
    check_senscoef(senscoef_dict)

    # Append the new dictionary to the current list
    params_dict.append(senscoef_dict)

    # Print terminal message if asked
    if info_filename is not None:
        print_msg(senscoef_dict, info_filename)


def check_senscoef(senscoef_dict):
    r"""Check the validity of the sensitivity coefficient data

    :param senscoef_data: (list of str) list of sensivitivity coefficient data
    """
    # Check the type
    if senscoef_dict["var_type"] != "scalar":
        raise TypeError("Only scalar type is supported for senscoef!")


def print_msg(param_dict, info_filename):
    r"""Write terminal message the results of parsing if verbosity asked

    :param info_filename: (str) the filename of the info_file
    :param param_dict: (dict) the parsed sensitivity coefficient parameters
    """
    with open(info_filename, "a") as info_file:
        info_file.writelines("***{:2d}***\n" .format(param_dict["enum"]))
        info_file.writelines("Sensitivity Coefficient with ID *{}* is "
                             "specified\n"
                             .format(param_dict["var_num"]))
        info_file.writelines("Parameter type: {}\n"
                             .format(param_dict["var_type"]))
        info_file.writelines("Parameter perturbation mode: {} ({})\n"
                             .format(param_dict["var_mode"],
                                     var_type_str(param_dict["var_mode"])))
        info_file.writelines("Parameter distribution: {}\n"
                             .format(param_dict["var_dist"]))
        info_file.writelines("1st distribution parameter: {:.3f}\n"
                             .format(param_dict["var_par1"]))
        info_file.writelines("2nd distribution parameter: {:.3f}\n"
                             .format(param_dict["var_par2"]))


def var_type_str(var_type):
    if var_type == 1:
        return "additive"
    elif var_type == 2:
        return "substitutive"
    elif var_type == 3:
        return "multiplicative"
