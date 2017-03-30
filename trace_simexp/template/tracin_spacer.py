# -*- coding: utf-8 -*-
"""
    trace_simexp.template.tracin_spacer
    ***********************************

    Module with functions to parse base TRACE input deck file for parameters
    related to spacer grid (``spacer``)
"""

__author__ = "Damar Wicaksono"


def get_nom_val(tracin_lines: list, param_dict: dict):
    r"""Get nominal value of spacer grid parameters from the tracin base

    :param tracin_lines: the base TRACE input deck
    :param param_dict: specification of the spacer grid parameter
    :return: (float) for all spacer grid parameters except "spmatid",
        (int) spacer grid material choices "spmatid"
    """
    import re

    nom_val = None

    # loop over lines
    for line_num, tracin_line in enumerate(tracin_lines):

        match = re.search(r"gridid", tracin_line, re.IGNORECASE)
        if match:

            gridid = int(tracin_lines[line_num+1].split()[0])
            # Check if the gridid is the correct
            if gridid == param_dict["var_num"]:

                # "var_card" specifies the line
                offset = 2 * param_dict["var_card"] - 1
                # "var_word" specifies the element in a line
                word = param_dict["var_word"] - 1
                nom_val = tracin_lines[line_num+offset].split()[word]
                break
        else:
            pass

    # all except "spmatid" (integer) are float
    if param_dict["var_name"] == "spmatid":
        return int(nom_val)
    else:
        return float(nom_val)


def put_key(tracin_lines: list, param_dict: dict) -> list:
    r"""Function to replace the nominal value of grid parameters with key

    the key is used for templating purpose and will later be substituted with
    sampled value

    :param tracin_lines: the base TRACE input deck
    :param param_dict: specification of spacer grid related parameters
    :return: the base TRACE input deck with line(s) replaced with key according
        to the grid parameters specification
    """
    import re
    from ..tracin_util import keygen

    # loop over lines
    for line_num, tracin_line in enumerate(tracin_lines):

        match = re.search(r"gridid", tracin_line, re.IGNORECASE)
        if match:

            gridid = int(tracin_lines[line_num+1].split()[0])
            # Check if the gridid is the correct
            if gridid == param_dict["var_num"]:

                # "var_card" specifies the line
                offset = 2 * param_dict["var_card"] - 1
                # "var_word" specifies the element in a line
                word = param_dict["var_word"] - 1
                # Replace the particular word with keys
                card = tracin_lines[line_num+offset].split()
                card[word] = keygen.create(param_dict, 
                                           template=True, 
                                           index=None)
                card = "".join("%14s" % k for k in card)
                # replace the line of tracin with the new one
                tracin_lines[line_num+offset] = card
                break
        else:
            pass

    return tracin_lines
