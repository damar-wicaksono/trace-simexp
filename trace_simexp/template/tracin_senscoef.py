# -*- coding: utf-8 -*-
"""
    trace_simexp.template.tracin_senscoef
    *************************************

    Module with functions to parse base TRACE input deck for parameters related
    to "sensitivity coefficient" (``senscoef``)
"""

__author__ = "Damar Wicaksono"


def get_nom_val(tracin_lines: list, param_dict: dict) -> float:
    r"""Get the nominal value of sensitivity coefficient from tracin base

    :param tracin_lines: the base TRACE input deck
    :param param_dict: specification of the senscoef parameter
    :return: the nominal value of the sensitivity coefficients
    """

    nom_val = None

    # loop over tracin lines
    for line_num, tracin_line in enumerate(tracin_lines):

        var_num = tracin_line.split()[0]        # safer to keep it as string
        if var_num == str(param_dict["var_num"]):
            # the sensitivity coefficient identifier is the beginning of line
            nom_val = float(tracin_line.split()[2])
            break
        else:
            continue

    return nom_val


def put_key(tracin_lines: list, param_dict: dict) -> list:
    r"""Function to replace the nominal value of senscoef parameters with key

    :param tracin_lines: the base TRACE input deck
    :param param_dict: specification of the senscoef parameter
    :return: the base TRACE input deck with line(s) modified according to
        the senscoef parameter key
    """
    from ..tracin_util import keygen

    word = 2    # the parameter values for senscoef is always at the 3rd values
    
    # loop over tracin lines
    for line_num, tracin_line in enumerate(tracin_lines):

        var_num = tracin_line.split()[0]        # safer to keep it as string
        if var_num == str(param_dict["var_num"]):
            # the sensitivity coefficient identifier is the beginning of line
            card = tracin_line.split()
            # Create the key and replace the word in the card
            card[word] = keygen.create(param_dict, template=True, index=None)
            # Sensitivity coefficient always have 3 cards
            card = "{:<8s}{:1s}{:>14s} " .format(card[0], card[1], card[2])
            # replace the line in tracin with the modified line
            tracin_lines[line_num] = card
            break
        else:
            continue

    return tracin_lines
