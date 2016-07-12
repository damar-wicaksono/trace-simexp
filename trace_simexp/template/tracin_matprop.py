"""Module with functionalities to parse tracin base for material property
"""

__author__ = "Damar Wicaksono"


# Default hard-coded values
MATPROP_TRACIN_KEY = "User Defined Material"
MATPROP_TABLE_KEY = "prptb"


def get_col_num(param_dict: dict) -> int:
    r"""Get the column number of a specified material property number
    
    Assign column number for each var_name, prptb consists of 7 columns
    the asterisk, prptb comment, temperature, rho, cp, cond, and emis 
    
    **Example**
    *  prptb         temp         rho          cp        cond        emis
    *  prptb*      273.15      8300.0       432.0        12.5         1.0s
    
    :param param_dict: the dictionary of the matprop parameter
    :return: the integer signifying column number, zero-indexed
    """
    if param_dict["var_name"] == "rho":
        col_var = 3
    elif param_dict["var_name"] == "cp":
        col_var = 4
    elif param_dict["var_name"] == "cond":
        col_var = 5
    elif param_dict["var_name"] == "emis":
        col_var = 6
    
    return col_var


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
    
    # Grab the column number based on var_name
    col_num = get_col_num(param_dict)

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
                        # Grab the specified parameter based on the "var_name"
                        val = tracin_lines[line_num+offset].split()[col_num]
                        if col_num != 6:
                            # no continuation, not the last column
                            nom_val.append(float(val))
                        else:
                            # last column has a continuation symbol, skip it
                            nom_val.append(float(val[:-1]))
                    offset += 1
                break
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
    r"""Replace the table type material property with key to be substituted

    :param tracin_lines: (list of str) the tracin base as a list of string
    :param param_dict: (dict) the dictionary of the matprop parameter
    :returns:(list of str) the modified base tracin with key for the matprop
        parameter as specified by param_dict
    """
    from ..tracin_util import keygen

    # Grab the column number based on var_name
    col_num = get_col_num(param_dict)

    # loop over tracin lines
    for line_num, tracin_line in enumerate(tracin_lines):
        if MATPROP_TRACIN_KEY in tracin_line:
            # match the keyword for material property specification block
            if str(param_dict["var_num"]) in tracin_line:
                # match the specified material number
                i = 0           # multiple values identifier in tabular format
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
                        cards = tracin_lines[line_num+offset]
                        cont = cards[-1]     # the continuation character
                        cards = cards.split()

                        # Create key, enclosed because of the continuation char
                        # three-value key due to enumeration of tabular values
                        key = keygen.create(param_dict, template=True, index=i)
                        # Replace the nominal value with key
                        cards[col_num] = key
                        # Replace the whole line with modified line with key                          
                        if col_num != 6:
                            # no continuation, not the last column
                             tracin_lines[line_num+offset] = \
                                 "{} {}{:>14s}{:>15s}{:>15s}{:>15s}{:>15s}" \
                                 .format(*cards)
                        else:
                            # last column has a continuation symbol
                            cards.append(cont)
                            tracin_lines[line_num+offset] = \
                                "{} {}{:>14s}{:>15s}{:>15s}{:>15s}{:>15s}{}" \
                                 .format(*cards)
                    
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