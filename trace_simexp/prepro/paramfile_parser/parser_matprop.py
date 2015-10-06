"""Module to parse material property specification from list of parameters file
"""

__author__ = "Damar Wicaksono"


def parse(line, params_dict, verbose=True):
    r"""Parse material property specification from a list of parameters file

    note that the input argument `params_dict` is mutable and will be modified

    :param line: (list of str) a line read from list of parameters file
    :param params_dict: (list of dict) the list of parameters in a dictionary
    :param verbose: (bool) terminal printing or not
    :returns: (list of dict) an updated params_dict with matprop specification
    """
    matprop_data = line.split()

    matprop_dict = {
        "enum": int(matprop_data[0]),
        "data_type": "matprop",
        "var_num": int(matprop_data[2]),
        "var_name": matprop_data[3].lower(),
        "var_type": matprop_data[4].lower(),
        "var_mode": int(matprop_data[5]),
        "var_card": int(matprop_data[6]),
        "var_word": int(matprop_data[7]),
        "var_dist": matprop_data[8].lower(),
        "var_par1": float(matprop_data[9]),
        "var_par2": float(matprop_data[10])
    }

    # Append the new dictionary to the current list
    params_dict.append(matprop_dict)

    if verbose:
        print_msg(matprop_dict)


def print_msg(matprop_dict):
    r"""Create a string to print on screen

    :param matprop_dict: (dict) the parsed component parameter
    """
    print("***{:2d}***" .format(matprop_dict["enum"]))
    print("Material ID *{}* property *{}* (Card *{}*)"
          .format(matprop_dict["var_num"],
                  matprop_dict["var_name"],
                  matprop_dict["var_card"]))
    print("Parameter type: {}" .format(matprop_dict["var_type"]))
    print("Parameter perturbation mode: {} ({})"
          .format(matprop_dict["var_mode"],
                  var_type_str(matprop_dict["var_mode"])))
    print("Parameter distribution: *{}*"
          .format(matprop_dict["var_dist"]))
    print("1st distribution parameter: {:.3e}"
          .format(matprop_dict["var_par1"]))
    print("2nd distribution parameter: {:.3e}"
          .format(matprop_dict["var_par2"]))


def var_type_str(var_type):
    if var_type == 1:
        return "substitutive"
    elif var_type == 2:
        return "additive"
    elif var_type == 3:
        return "multiplicative"
