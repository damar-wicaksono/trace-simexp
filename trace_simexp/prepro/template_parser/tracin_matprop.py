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
        nom_val = read_fit(tracin_lines, param_dict)
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
                offset += 1     # one more line as the first prptb is a header
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


def put_key(tracin_lines, param_dict):
    r"""Replace the nominal value of matprop parameter with key

    :param tracin_lines: (list of str) the tracin base as a list of string
    :param param_dict: (dict) the dictionary of the matprop parameter
    :returns:(list of str) the modified base tracin with key for the parameter
        as specified by param_dict
    """

    if param_dict["var_type"] == "table":
        tracin_lines = edit_table(tracin_lines, param_dict)
    elif param_dict["var_type"] == "fit":
        tracin_lines = edit_fit(tracin_lines, param_dict)
    else:
        raise TypeError("Not recognized material property type variable")

    return tracin_lines


def edit_table(tracin_lines, param_dict):
    r"""Get the nominal values of table-type matprop parameters

    :param tracin_lines: (list of str) the tracin base as a list of string
    :param param_dict: (dict) the dictionary of the matprop parameter
    :returns:(list of str) the modified base tracin with key for the matprop
        parameter as specified by param_dict
    """

    # loop over tracin lines
    for line_num, tracin_line in enumerate(tracin_lines):
        if MATPROP_TRACIN_KEY in tracin_line:
            # match the keyword for material property specification block
            if str(param_dict["var_num"]) in tracin_line:
                # match the specified material number
                i = 1           # multiple values identifier in tabular format
                offset = 0
                while True:
                    # loop to go to where the values defined
                    if MATPROP_TABLE_KEY in tracin_lines[line_num+offset]:
                        break
                    else:
                        pass
                    offset += 1
                offset += 1     # one more line as the first prptb is a header
                while True:
                    # loop to get the values
                    if MATPROP_TABLE_KEY not in tracin_lines[line_num+offset]:
                        break
                    else:
                        # Grab the card and split the string
                        card = tracin_lines[line_num+offset]
                        cont = card[-1]     # the continuation character
                        card = card.split()

                        # Create key, enclosed because of the continuation char
                        # three-value key due to enumeration of tabular values
                        key = "${{{}_{}_{}}}" .format(param_dict["var_name"],
                                                  param_dict["enum"],
                                                  i)
                        # Replace the nominal value with key
                        col_num = param_dict["var_card"] + 2 # offset column
                        card[col_num] = key

                        # Replace the whole line with modified line
                        if param_dict["var_card"] != 4:
                            # no continuation , matprop definitely has 5 columns
                             tracin_lines[line_num+offset] = \
                                 "{} {}{:>14s}{:>14s}{:>14s}{:>14s}{:>14s}" \
                                 .format(card[0], card[1], card[2],
                                         card[3], card[4], card[5], card[6])
                        else:
                            # last column has a continuation symbol, skip it
                            tracin_lines[line_num+offset] = \
                                "{} {}{:>14s}{:>14s}{:>14s}{:>14s}{:>14s}{}" \
                                 .format(card[0], card[1], card[2],
                                         card[3], card[4], card[5],
                                         card[6], cont)


                    offset += 1
                    i += 1
                break

    return tracin_lines


def edit_fit(tracin_lines, param_dict):
    r"""Get the nominal values of fit-type matprop parameters

    :param tracin_lines: (list of str) the tracin base as a list of string
    :param param_dict: (dict) the dictionary of the matprop parameter
    :returns:(list of str) the modified base tracin with key for the matprop
        parameter as specified by param_dict
    """
    # TODO: Complete edit_fit function()
    return None