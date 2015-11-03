"""Module to parse material property specification from list of parameters file
"""

__author__ = "Damar Wicaksono"


def parse(line, params_dict, info_filename=None):
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
        "var_par2": float(matprop_data[10]),
        "str_fmt": matprop_data[11]
    }

    # Append the new dictionary to the current list
    params_dict.append(matprop_dict)

    if info_filename is not None:
        print_msg(matprop_dict, info_filename)


def print_msg(matprop_dict, info_filename):
    r"""Create a string to print on screen

    :param info_filename: (str) the filename of the info_file
    :param matprop_dict: (dict) the parsed component parameter
    """
    with open(info_filename, "a") as info_file:
        info_file.writelines("***{:2d}***\n" .format(matprop_dict["enum"]))
        info_file.writelines("Material ID *{}* property *{}* (Card *{}*)\n"
                             .format(matprop_dict["var_num"],
                                     matprop_dict["var_name"],
                                     matprop_dict["var_card"]))
        info_file.writelines("Parameter type: {}\n"
                             .format(matprop_dict["var_type"]))
        info_file.writelines("Parameter perturbation mode: {} ({})\n"
                             .format(matprop_dict["var_mode"],
                                     var_type_str(matprop_dict["var_mode"])))
        info_file.writelines("Parameter distribution: *{}*\n"
                             .format(matprop_dict["var_dist"]))
        info_file.writelines("1st distribution parameter: {:.3e}\n"
                             .format(matprop_dict["var_par1"]))
        info_file.writelines("2nd distribution parameter: {:.3e}\n"
                             .format(matprop_dict["var_par2"]))


def var_type_str(var_type):
    if var_type == 1:
        return "additive"
    elif var_type == 2:
        return "substitutive"
    elif var_type == 3:
        return "multiplicative"
