"""Module to parse material property specification from list of parameters file
"""

__author__ = "Damar Wicaksono"


def parse(line) -> dict:
    """Parse material property specification from a list of parameters file

    :param line: (list of str) a line read from list of parameters file
    :returns: (dict) the parsed input parameter with pre-specified key
    """
    matprop_data = line.split()

    matprop_dict = {
        "enum": int(matprop_data[0]),
        "data_type": "matprop",
        "var_num": int(matprop_data[2]),
        "var_name": matprop_data[3].lower(),
        "var_type": matprop_data[4].lower(),
        "var_card": matprop_data[5],
        "var_word": matprop_data[6],
        "var_mode": int(matprop_data[7]),
        "var_dist": matprop_data[8].lower(),
        "var_par1": float(matprop_data[9]),
        "var_par2": float(matprop_data[10]),
        "str_fmt": matprop_data[11]
    }

    # Add the message to be written in prepro.info
    matprop_dict["str_msg"] = create_msg(matprop_dict)

    return matprop_dict


def create_msg(matprop_dict) -> list:
    """Create a string of parsed parameters

    :param matprop_dict: (dict) the parsed component parameter
    """
    from .common import var_type_str

    str_msg = list()

    str_msg.append("***{:2d}***" .format(matprop_dict["enum"]))
    str_msg.append("Material ID *{}* property *{}* (Card *{}*)"
                   .format(matprop_dict["var_num"],
                           matprop_dict["var_name"],
                           matprop_dict["var_card"]))
    str_msg.append("Parameter type: {}" .format(matprop_dict["var_type"]))
    str_msg.append("Parameter perturbation mode: {} ({})"
                   .format(matprop_dict["var_mode"],
                           var_type_str(matprop_dict["var_mode"])))
    str_msg.append("Parameter distribution: *{}*"
                   .format(matprop_dict["var_dist"]))
    str_msg.append("1st distribution parameter: {:.3e}"
                   .format(matprop_dict["var_par1"]))
    str_msg.append("2nd distribution parameter: {:.3e}\n"
                   .format(matprop_dict["var_par2"]))

    return "\n".join(str_msg)
