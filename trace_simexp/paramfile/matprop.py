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
        "var_mode": int(matprop_data[5]),
        "var_card": int(matprop_data[6]),
        "var_word": int(matprop_data[7]),
        "var_dist": matprop_data[8].lower(),
        "var_par1": float(matprop_data[9]),
        "var_par2": float(matprop_data[10]),
        "str_fmt": matprop_data[11]
    }

    return matprop_dict
