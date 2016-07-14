"""Module to parse component parameter data from list of parameters file
"""

__author__ = "Damar Wicaksono"


def parse(line) -> dict:
    """Parse component parameter specification from a list of parameters file

    :param line: (list of str) a line read from list of parameters file
    :returns: (dict) the parsed input parameter with pre-specified key
    """
    from .common import parse_var_params

    comp_data = line.split()

    # Check the validity of the component data
    check_comp(comp_data)

    comp_dict = {
        "enum": int(comp_data[0]),
        "data_type": comp_data[1],
        "var_num": int(comp_data[2]),
        "var_name": comp_data[3].lower(),
        "var_type": comp_data[4].lower(),
        "var_card": int(comp_data[5]),
        "var_word": int(comp_data[6]),
        "var_mode": int(comp_data[7]),
        "var_dist": comp_data[8].lower(),
        "var_pars": parse_var_params(line),
        "str_fmt": comp_data[-1]
    }

    # Add the message to be written in prepro.info
    comp_dict["str_msg"] = create_msg(comp_dict)

    return comp_dict


def create_msg(comp_dict: dict) -> str:
    """Create a string of parsed parameters

    :param comp_dict: (dict) the parsed component parameter
    """
    from .common import var_type_str
    from .common import print_var_params

    str_msg = list()

    str_msg.append("***{:2d}***" .format(comp_dict["enum"]))
    str_msg.append("Component *{}* ID *{}*, parameter *{}* is "
                   "specified" .format(comp_dict["data_type"],
                                       comp_dict["var_num"],
                                       comp_dict["var_name"]))
    str_msg.append("Parameter type: {}"
                   .format(comp_dict["var_type"]))
    str_msg.append("Parameter perturbation mode: {} ({})"
                   .format(comp_dict["var_mode"],
                           var_type_str(comp_dict["var_mode"])))
    str_msg.append("Parameter Probability Distribution:")
    str_msg.append(" - distribution: *{}*"
                   .format(comp_dict["var_dist"]))
    str_msg.append(print_var_params(comp_dict["var_pars"]))

    return "\n".join(str_msg)


def check_comp(comp_data):
    r"""Check the validity of component data

    :param comp_data: (list) list of specifications for spacer grid data
    """
    # list of supported components
    comps = ["pipe", "vessel", "power", "fill", "break"]

    if not comp_data[1] in comps:
        raise TypeError("*{}* component is not currently supported"
                        .format(comp_data[1]))
