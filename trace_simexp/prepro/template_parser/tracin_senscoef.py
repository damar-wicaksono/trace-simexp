"""Module with functionalities to parse tracin base for sensitivity coefficient
"""

__author__ = "Damar Wicaksono"


def get_nom_val(tracin_lines, param_dict):
    r"""Get the nominal values of sensitivity coefficient from tracin base

    :param tracin_lines: (list of str) the tracin base in python list
    :param param_dict: (dict) the dictionary of senscoef parameter
    :returns: (float) the nominal value of the sensitivity coefficients
    """

    nom_val = None

    # loop over tracin lines
    for line_num, tracin_line in enumerate(tracin_lines):

        var_num = tracin_line.split()[0]            # safer to keep it as string
        if var_num == str(param_dict["var_num"]):
            # the sensitivity coefficient identifier is the beginning of line
            nom_val = float(tracin_line.split()[2])
        else:
            continue

    return nom_val

