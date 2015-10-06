"""Module to parse component parameter data from list of parameters file
"""

__author__ = "Damar Wicaksono"


def parse(line, params_dict, verbose=True):
    r"""Parse component parameter specification from a list of parameters file

    note that the input argument `params_dict` is mutable and will be modified

    :param line: (list of str) a line read from list of parameters file
    :param params_dict: (list of dict) the list of parameters in a dictionary
    :param verbose: (bool) terminal printing or not
    :returns: (list of dict) an updated params_dict with comp specification
    """
    comp_data = line.split()

    # Check the validity of the component data
    check_comp(comp_data)

    comp_dict = {
        "enum": int(comp_data[0]),
        "data_type": comp_data[1],
        "var_num": int(comp_data[2]),
        "var_name": comp_data[3].lower(),
        "var_type": comp_data[4].lower(),
        "var_mode": int(comp_data[5]),
        "var_card": int(comp_data[6]),
        "var_word": int(comp_data[7]),
        "var_dist": comp_data[8].lower(),
        "var_par1": float(comp_data[9]),
        "var_par2": float(comp_data[10])
    }

    # Append the new dictionary to the current list
    params_dict.append(comp_dict)

    if verbose:
        print_msg(comp_dict)


def print_msg(comp_dict):
    r"""Create a string to print on screen

    :param comp_dict: (dict) the parsed component parameter
    """
    print("***{:2d}***" .format(comp_dict["enum"]))
    print("Component *{}* ID *{}*, parameter *{}* is specified"
          .format(comp_dict["data_type"],
                  comp_dict["var_num"],
                  comp_dict["var_name"]))
    print("Parameter type: {}" .format(comp_dict["var_type"]))
    print("Parameter perturbation mode: {} ({})"
          .format(comp_dict["var_mode"],
                  var_type_str(comp_dict["var_mode"])))
    print("Parameter distribution: *{}*"
          .format(comp_dict["var_dist"]))
    print("1st distribution parameter: {:.3e}"
          .format(comp_dict["var_par1"]))
    print("2nd distribution parameter: {:.3e}"
          .format(comp_dict["var_par2"]))


def check_comp(comp_data):
    r"""Check the validity of component data

    :param comp_data: (list) list of specifications for spacer grid data
    """
    # list of supported components
    comps = ["pipe", "vessel", "power", "fill", "break"]

    if not comp_data[1] in comps:
        raise TypeError("*{}* component is not currently supported"
                        .format(comp_data[1]))


def var_type_str(var_type):
    if var_type == 1:
        return "substitutive"
    elif var_type == 2:
        return "additive"
    elif var_type == 3:
        return "multiplicative"