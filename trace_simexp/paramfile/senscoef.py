"""Module to parse sensitivity coefficient data from the list of parameters file
"""

__author__ = "Damar Wicaksono"


def parse(line) -> dict:
    """Parse sensitivity coefficient specification from list of parameters file

    :param line: (list of str) a line read from list of parameters file
    :returns: (dict) the parsed input parameter with pre-specified key
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

    # Add the message to be written in prepro.info
    senscoef_dict["str_msg"] = create_msg(senscoef_dict)

    return senscoef_dict


def check_senscoef(senscoef_dict):
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

    str_msg = list()

    str_msg.append("***{:2d}***" .format(senscoef_dict["enum"]))
    str_msg.append("Sensitivity Coefficient with ID *{}* is specified"
                   .format(senscoef_dict["var_num"]))
    str_msg.append("Parameter type: {}" .format(senscoef_dict["var_type"]))
    str_msg.append("Parameter perturbation mode: {} ({})"
                   .format(senscoef_dict["var_mode"],
                           var_type_str(senscoef_dict["var_mode"])))
    str_msg.append("Parameter distribution: {}"
                   .format(senscoef_dict["var_dist"]))
    str_msg.append("1st distribution parameter: {:.3f}"
                   .format(senscoef_dict["var_par1"]))
    str_msg.append("2nd distribution parameter: {:.3f}\n"
                   .format(senscoef_dict["var_par2"]))

    return "\n".join(str_msg)
