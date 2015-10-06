"""Module with functionalities to parse tracin base for component parameters
"""

__author__ = "Damar Wicaksono"


def get_nom_val(tracin_lines, param_dict):
    r"""Get the nominal values of component parameters from tracin base file

    :param tracin_lines: (list of str) the tracin base as a list
    :param param_dict: (dict) the dictionary of the comp parameter
    :return: (list) the nominal values of the comp parameter
    """
    nom_val = None

    # select the type of variable
    if param_dict["var_type"] == "scalar":
        nom_val = read_scalar(tracin_lines, param_dict)
    elif param_dict["var_type"] == "table":
        nom_val = read_table(tracin_lines, param_dict)
    elif param_dict["var_type"] == "array":
        nom_val = read_array(tracin_lines, param_dict)
    else:
        raise TypeError("Component parameter variable type not recognized!")

    return nom_val


def read_scalar(tracin_lines, param_dict):
    r"""Get the nominal values of scalar-type component parameters

    Scalar-type component parameters are straightforward. Their location is
    directly defined by the card and word identifiers.

    :param tracin_lines: (list of str) the tracin base as a list
    :param param_dict: (dict) the dictionary of the comp parameter
    :return: (float or int) the nominal values of the comp parameter
    """
    nom_val = None

    # loop over lines
    for line_num, tracin_line in enumerate(tracin_lines):
        if tracin_line.startswith(param_dict["data_type"]):
            # Check if the number corresponds to what specified
            if str(param_dict["var_num"]) in tracin_line:
                # "var_card" specify the line
                offset = 2 * param_dict["var_card"] - 2
                # "var_word" specify the element
                word = param_dict["var_word"] - 1
                # grab the nominal value
                nom_val = tracin_lines[line_num+offset].split()[word]

                # check what kind of numeric is nom_val
                if "." in nom_val:
                    # float
                    nom_val = float(nom_val)
                elif "E" in nom_val or "e" in nom_val:
                    # float in scientific notation
                    nom_val = float(nom_val)
                else:
                    # integer
                    nom_val = int(nom_val)
    return nom_val


def read_table(tracin_lines, param_dict):
    r"""Get the nominal values of tabular-type component parameters

    Tabular-type refers to the type that is a set of multiple values of
    different type. e.g., time - power pair, time - velocity pair etc. These
    values are defined in tracin as a single long sequence (over multiple lines
    with continuation), but their definition changed.

    :param tracin_lines: (list of str) the tracin base as a list
    :param param_dict: (dict) the dictionary of the comp parameter
    :return: (list) the nominal values of the comp parameter
    """
    import re

    nom_val = []

    # loop over lines
    for line_num, tracin_line in enumerate(tracin_lines):
        if tracin_line.startswith(param_dict["data_type"]):
            # Check if the number corresponds to what specified
            if str(param_dict["var_num"]) in tracin_line:
                offset = 0
                while True:
                    # loop to go the line where the parameter is first specified
                    if param_dict["var_name"] in tracin_lines[line_num+offset]:
                        break
                    else:
                        pass
                    offset += 1
                while True:
                    # loop to read all the available nominal values
                    if param_dict["var_name"] not in tracin_lines[line_num+offset]:
                        break
                    else:
                        # grab the line and take only numerical values
                        vals = re.findall(r"\d+[\.]?\d*[Ee]?\d+",
                                          tracin_lines[line_num+offset])
                        # grab the value according to the "var_word"
                        nom_val.append(float(vals[param_dict["var_card"]-1]))
                    offset += 1
    return nom_val


def read_array(tracin_lines, param_dict):
    r"""Get the nominal values of array-type component parameters

    Array time simply means that all values are of single type, not a set of
    types (e.g., time - power pair). Initial fluid velocity in a pipe is an
    array type variable.

    :param tracin_lines: (list of str) the tracin base as a list
    :param param_dict: (dict) the dictionary of the comp parameter
    :return: (list) the nominal values of the comp parameter
    """
    # TODO: Complete read_array function()
    return None
