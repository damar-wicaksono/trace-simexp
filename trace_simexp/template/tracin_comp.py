# -*- coding: utf-8 -*-
"""
    trace_simexp.template.tracin_comp
    *********************************

    Module with functions to parse the base TRACE input deck for parameters
    related to TRACE component (``comp``)
"""

__author__ = "Damar Wicaksono"


def get_nom_val(tracin_lines: list, param_dict: dict):
    r"""Get the nominal values of component parameters from tracin base file

    :param tracin_lines: the base TRACE input deck
    :param param_dict: specification of the comp parameter
    :return: the nominal values of the comp parameter
    """

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


def read_scalar(tracin_lines: list, param_dict: dict):
    r"""Get the nominal values of scalar-type component parameters

    Scalar-type component parameters are straightforward. Their location is
    directly defined by the card and word identifiers.

    :param tracin_lines: the base TRACE input deck
    :param param_dict: specification of the comp parameter
    :return: the nominal values of the comp parameter specified as scalar.
        Possible types - float and integer
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
                if "E" in nom_val or "e" in nom_val:
                    # float in scientific notation
                    nom_val = float(nom_val)
                elif "." in nom_val:
                    # float
                    nom_val = float(nom_val)
                else:
                    # integer
                    nom_val = int(nom_val)

                break

    return nom_val


def read_table(tracin_lines: list, param_dict: dict) -> list:
    r"""Get the nominal values of tabular-type component parameters

    Tabular-type refers to the type that is a set of multiple values of
    different type. e.g., time - power pair, time - velocity pair etc. These
    values are defined in tracin as a single long sequence (over multiple lines
    with continuation), but their definition changed.

    :param tracin_lines: the base TRACE input deck
    :param param_dict: specification of the comp parameter
    :return: the nominal values of the comp parameter specified as table
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
                    # loop to go the line where the parameter is 1st specified
                    if param_dict["var_name"] in tracin_lines[line_num+offset]:
                        break
                    else:
                        pass
                    offset += 1
                while True:
                    # loop to read all the available nominal values
                    if param_dict["var_name"] not in \
                            tracin_lines[line_num+offset]:
                        break
                    else:
                        # grab the line and take only numerical values
                        vals = re.findall(r"\d+[\.]?\d*[Ee]?\d+",
                                          tracin_lines[line_num+offset])
                        # grab the value according to the "var_word"
                        nom_val.append(float(vals[param_dict["var_card"]-1]))
                    offset += 1
                break

    return nom_val


def read_array(tracin_lines: list, param_dict: dict) -> list:
    r"""Get the nominal values of array-type component parameters

    Array time simply means that all values are of single type, not a set of
    types (e.g., time - power pair). Initial fluid velocity in a pipe is an
    array type variable defined for each faces.

    :param tracin_lines: the base TRACE input deck
    :param param_dict: specification of the comp parameter
    :return: the nominal values of the comp parameter specified as array
    """
    # TODO: Complete read_array function()
    return []


def put_key(tracin_lines: list, param_dict: dict) -> list:
    r"""Replace the nominal value of component parameter with key

    :param tracin_lines: the base TRACE input deck
    :param param_dict: specification of the comp parameter
    :returns: the modified base TRACE input deck with key for the parameter
        as specified by param_dict
    """
    # select the type of variable
    if param_dict["var_type"] == "scalar":
        tracin_lines = edit_scalar(tracin_lines, param_dict)
    elif param_dict["var_type"] == "table":
        tracin_lines = edit_table(tracin_lines, param_dict)
    elif param_dict["var_type"] == "array":
        tracin_lines = edit_array(tracin_lines, param_dict)
    else:
        raise TypeError("Component parameter variable type not recognized!")

    return tracin_lines


def edit_scalar(tracin_lines: list, param_dict: dict) -> list:
    r"""Replace the nominal value of scalar-type component parameters with key

    Scalar-type component parameters are straightforward. Their location is
    directly defined by the card and word identifiers.

    :param tracin_lines: the base TRACE input deck
    :param param_dict: specification of the comp parameter, scalar type
    :return: the modified base TRACE input deck with key for the parameter
        as specified by param_dict
    """
    from ..tracin_util import keygen

    # loop over lines
    for line_num, tracin_line in enumerate(tracin_lines):
        if tracin_line.startswith(param_dict["data_type"]):
            # Check if the number corresponds to what specified
            if str(param_dict["var_num"]) in tracin_line:
                # "var_card" specify the line, grab the card
                offset = 2 * param_dict["var_card"] - 2
                card = tracin_lines[line_num+offset].split()
                # "var_word" specify the element
                word = param_dict["var_word"] - 1
                # Replace the word in the card
                card[word] = keygen.create(param_dict, 
                                           template=True, 
                                           index=None)
                # concatenate the list of string to remake the card
                card = "".join("%14s" % k for k in card)
                # replace the input with modified card
                tracin_lines[line_num+offset] = card

                break

    return tracin_lines


def edit_table(tracin_lines: list, param_dict: dict) -> list:
    r"""Replace the nominal values of table-type component parameters with keys

    :param tracin_lines: the base TRACE input deck
    :param param_dict: specification of the comp parameter, table type
    :return: the modified base TRACE input deck with key for the parameter
        as specified by param_dict
    """
    import re
    from ..tracin_util import keygen

    # loop over lines
    for line_num, tracin_line in enumerate(tracin_lines):
        if tracin_line.startswith(param_dict["data_type"]):
            # Check if the number corresponds to what specified
            if str(param_dict["var_num"]) in tracin_line:
                i = 0   # table multiple values identifier
                offset = 0
                while True:
                    # loop to go the line where the parameter is 1st specified
                    if param_dict["var_name"] in tracin_lines[line_num+offset]:
                        break
                    else:
                        pass
                    offset += 1
                while True:
                    # loop to replace all the available nominal values
                    if param_dict["var_name"] not in \
                            tracin_lines[line_num+offset]:
                        break
                    else:
                        # grab the comment in the line
                        comment = re.findall(r"\*\s*\w*\s*\*",
                                             tracin_lines[line_num+offset])[0]
                        # grab the line and take only numerical values
                        vals = re.findall(r"\d+[\.]?\d*[Ee]?\d+",
                                          tracin_lines[line_num+offset])
                        # grab the continuation character
                        cont = re.findall(r".$",
                                          tracin_lines[line_num+offset])[0]
                        # Create key, enclosed because of the continuation char
                        # three-value key due to enumeration of tabular values
                        key = keygen.create(param_dict, template=True, index=i)
                        # replace the value according to the "var_word" w/ key
                        vals[param_dict["var_card"]-1] = key
                        vals = "".join("%15s" % k for k in vals)

                        # Replace the line with modified line
                        tracin_lines[line_num+offset] = "{} {}{}" .format(
                            comment, vals, cont
                        )

                    i += 1
                    offset += 1

                break

    return tracin_lines


def edit_array(tracin_lines: list, param_dict: dict) -> list:
    r"""Get the nominal values of array-type component parameters

    Array time simply means that all values are of single type, not a set of
    types (e.g., time - power pair). Initial fluid velocity in a pipe is an
    array type variable.

    :param tracin_lines: the base TRACE input deck
    :param param_dict: specification of the comp parameter, array type
    :return: the modified base TRACE input deck with key for the parameter
        as specified by param_dict
    """
    # TODO: Complete edit_array function()
    return []
