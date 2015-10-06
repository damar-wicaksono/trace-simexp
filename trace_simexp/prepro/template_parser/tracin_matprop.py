"""Module with functionalities to parse tracin base for material property
"""

__author__ = "Damar Wicaksono"


MATPROP_TRACIN_KEY = "User Defined Material"
MATPROP_TABLE_KEY = "prptb"

def get_nom_val(tracin_lines, param_dict):
    r"""Get the nominal value of material property parameter from tracin base

    :param tracin_lines: (list of str) the tracin base as a list
    :param param_dict: (dict) the dictionary of the matprop parameter
    :return: (list) the nominal values of the matprop parameter
    """
    nom_val = None

    if param_dict["var_type"] == "table":
        nom_val = read_table(tracin_lines, param_dict)
    elif param_dict["var_type"] == "fit":
        nom_val = read_table(tracin_lines, param_dict)
    else:
        raise TypeError("Not recognized material property type variable")

    return nom_val


def read_table(tracin_lines, param_dict):
    r"""Get the nominal value of table-type material property parameter

    :param tracin_lines: (list of str) the tracin base as a list
    :param param_dict: (dict) the dictionary of the matprop parameter
    :return: (list) the nominal values of the matprop parameter
    """
    nom_val = []

    # loop over tracin lines
    for line_num, tracin_line in enumerate(tracin_lines):
        if MATPROP_TRACIN_KEY in tracin_line:
            # match the keyword for material property specification block
            if str(param_dict["var_num"]) in tracin_line:
                # match the specified material number
                offset = 0
                while True:
                    # loop to go to where the values defined
                    if MATPROP_TABLE_KEY in tracin_lines[line_num+offset]:
                        break
                    else:
                        pass
                    offset += 1
                offset += 1     # one more line as the first prtpb is a header
                while True:
                    # loop to get the values
                    if MATPROP_TABLE_KEY not in tracin_lines[line_num+offset]:
                        break
                    else:
                        # Grab the specified parameter based on the "var_card"
                        col_num = param_dict["var_card"] + 2 # offset column
                        val = tracin_lines[line_num+offset].split()[col_num]
                        if param_dict["var_card"] != 4:
                            # no continuation , matprop definitely has 5 columns
                            nom_val.append(float(val))
                        else:
                            # last column has a continuation symbol, skip it
                            nom_val.append(float(val[:-1]))
                    offset += 1
    return nom_val


def read_fit(tracin_lines, param_dict):
    r"""Get the nominal value of fit-type material property parameter

    :param tracin_lines: (list of str) the tracin base as a list
    :param param_dict: (dict) the dictionary of the matprop parameter
    :return: (array) the nominal values of the matprop parameter
    """
    # TODO: Complete the specification of parsing fit material type
    return None