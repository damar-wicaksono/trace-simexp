"""Module with functionalities to parse tracin base file for spacer grid params
"""

__author__ = "Damar Wicaksono"


def get_nom_val(tracin_lines, param_dict):
    r"""Get nominal values of spacer grid parameters from the tracin base

    :param tracin_lines: (list of str) the tracin read into python as list
    :param param_dict: (dict) dictionary of the parameter to be updated
    :returns: (float) for all spacer grid parameters except "spmatid"
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
        else:
            pass

    # all except "spmatid" (integer) are float
    if param_dict["var_name"] == "spmatid":
        return int(nom_val)
    else:
        return float(nom_val)