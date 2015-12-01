"""Module to parse component parameter data from list of parameters file
"""

__author__ = "Damar Wicaksono"


def parse(line) -> dict:
    """Parse component parameter specification from a list of parameters file

    :param line: (list of str) a line read from list of parameters file
    :returns: (dict) the parsed input parameter with pre-specified key
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
        "var_par2": float(comp_data[10]),
        "str_fmt": comp_data[11]
    }

    return comp_dict


def print_msg(comp_dict, info_filename):
    r"""Create a string to print on screen

    :param info_filename: (str) the filename of the info_file
    :param comp_dict: (dict) the parsed component parameter
    """
    with open(info_filename, "a") as info_file:
        info_file.writelines("***{:2d}***\n" .format(comp_dict["enum"]))
        info_file.writelines("Component *{}* ID *{}*, parameter *{}* is "
                             "specified\n" .format(comp_dict["data_type"],
                                                   comp_dict["var_num"],
                                                   comp_dict["var_name"]))
        info_file.writelines("Parameter type: {}\n"
                             .format(comp_dict["var_type"]))
        info_file.writelines("Parameter perturbation mode: {} ({})\n"
                             .format(comp_dict["var_mode"],
                                     var_type_str(comp_dict["var_mode"])))
        info_file.writelines("Parameter distribution: *{}*\n"
                             .format(comp_dict["var_dist"]))
        info_file.writelines("1st distribution parameter: {:.3e}\n"
                             .format(comp_dict["var_par1"]))
        info_file.writelines("2nd distribution parameter: {:.3e}\n"
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
        return "additive"
    elif var_type == 2:
        return "substitutive"
    elif var_type == 3:
        return "multiplicative"