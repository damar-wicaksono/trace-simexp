"""Module to parse sensitivity coefficient data from the list of parameters file
"""

__author__ = "Damar Wicaksono"


def parse(line) -> dict:
    """Parse sensitivity coefficient specification from list of parameters file

    :param line: (list of str) a line read from list of parameters file
    :returns: (dict) the parsed input parameter with pre-specified key
    """
    from .common import parse_var_params

    senscoef_data = line.split()

    senscoef_dict = {
        "enum": int(senscoef_data[0]),
        "data_type": "senscoef",
        "var_num": int(senscoef_data[2]),
        "var_name": None,
        "var_type": senscoef_data[4].lower(),
        "var_card": None,
        "var_word": None,
        "var_mode": int(senscoef_data[7]),
        "var_dist": senscoef_data[8].lower(),
        "var_pars": parse_var_params(line),
        "str_fmt": senscoef_data[11]
    }

    # Check the validity
    check_senscoef(senscoef_dict)

    # Add the message to be written in prepro.info
    senscoef_dict["str_msg"] = create_msg(senscoef_dict)

    return senscoef_dict


def check_senscoef(senscoef_dict: dict):
    r"""Check the validity of the sensitivity coefficient data

    :param senscoef_data: (list of str) list of sensivitivity coefficient data
    """
    # Check the type
    if senscoef_dict["var_type"] != "scalar":
        raise TypeError("Only scalar type is supported for senscoef!")


def create_msg(senscoef_dict: dict) -> str:
    """Create a string of parsed parameters

    :param senscoef_dict: (dict) the parsed sensitivity coefficient parameters
    """
    from .common import var_type_str
    from .common import print_var_params

    str_msg = list()

    str_msg.append("***{:2d}***" .format(senscoef_dict["enum"]))
    str_msg.append("Sensitivity Coefficient with ID *{}* is specified"
                   .format(senscoef_dict["var_num"]))
    str_msg.append("Parameter type: {}" .format(senscoef_dict["var_type"]))
    str_msg.append("Parameter perturbation mode: {} ({})"
                   .format(senscoef_dict["var_mode"],
                           var_type_str(senscoef_dict["var_mode"])))
    str_msg.append("Perturbation factor probability distribution:")
    str_msg.append(" - distribution: *{}*"
                   .format(senscoef_dict["var_dist"]))
    str_msg.append(print_var_params(senscoef_dict["var_pars"]))

    return "\n".join(str_msg)
