"""Module to parse sensitivity coefficient data from the list of parameters file
"""

__author__ = "Damar Wicaksono"


def parse_senscoef(line, params_dict, verbose=True):
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
        "var_mode": senscoef_data[5],
        "var_card": None,
        "var_word": None,
        "var_dist": senscoef_data[8],
        "var_par1": float(senscoef_data[9]),
        "var_par2": float(senscoef_data[10])
    }

    # Check the validity
    check_senscoef(senscoef_dict)

    # Append the new dictionary to the current list
    params_dict.append(senscoef_dict)

    # Print terminal message if asked
    if verbose:
        print_msg(senscoef_dict)


def check_senscoef(senscoef_dict):
    r"""Check the validity of the sensitivity coefficient data

    :param senscoef_data: (list of str) list of sensivitivity coefficient data
    """
    # Check the type
    if senscoef_dict["var_type"] != "scalar":
        raise TypeError("Only scalar type is supported for senscoef!")


def print_msg(param_dict):
    r"""Write terminal message the results of parsing if verbosity asked

    :param param_dict: (dict) the parsed sensitivity coefficient parameters
    """
    print("***{:2d}***" .format(param_dict["enum"]))
    print("Sensitivity Coefficient with ID *{}* is specified"
          .format(param_dict["var_num"]))
    print("Parameter type: {}" .format(param_dict["var_type"]))
    print("Parameter perturbation mode: {} ({})"
          .format(param_dict["var_mode"],
                  var_type_str(int(param_dict["var_mode"]))))
    print("Parameter distribution: {}" .format(param_dict["var_dist"]))
    print("1st distribution parameter: {:.3f}" .format(param_dict["var_par1"]))
    print("2nd distribution parameter: {:.3f}" .format(param_dict["var_par2"]))


def var_type_str(var_type):
    if var_type == 1:
        return "scalar, substitutive"
    elif var_type == 2:
        return "scalar, additive"
    elif var_type == 3:
        return "scalar, multiplicative"
