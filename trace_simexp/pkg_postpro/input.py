"""Module to get all the required inputs for post-processing phase
"""

__author__ = "Damar Wicaksono"


def read_tracevars(vars_fullname: str) -> list:
    """Read the list of trace variables to be extracted from xtv/dmx file
    """
    vars_list = list()

    with open(vars_fullname, "rt") as vars_file:
        vars_lines = vars_file.read().splitlines()

    for vars_line in vars_lines:
        vars_list.append(vars_line.split("#")[0].strip())

    return vars_list



