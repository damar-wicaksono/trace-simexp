"""Module to read list of TRACE graphic variable files and create an aptscript
command
"""


__author__ = "Damar Wicaksono"


def read(vars_filename: str) -> list:
    """Read the list of trace variables to be extracted from xtv/dmx file

    :param vars_filename: (str) the list of TRACE graphic variables to be
        extracted, fullname
    :returns: (list) the list of TRACE graphic variables in string
    """
    vars_list = list()

    with open(vars_filename, "rt") as vars_file:
        vars_lines = vars_file.read().splitlines()

    for vars_line in vars_lines:
        vars_list.append(vars_line.split("#")[0].strip())

    return vars_list


def make_apt(run_filename: str, trace_vars: list, xtv_ext="dmx") -> list:
    """Function to create an aptplot input file according to the requested vars

    :return: a list of string of aptplot command in batch mode
    """
    apt_script = list()

    apt_script.append("TRAC 0 XTV {}.{}" .format(run_filename, xtv_ext))

    for trace_var in trace_vars:
        apt_script.append("TREAD 0 \"{}\" SIU" .format(trace_var))

    apt_script.append("TRAC 0 EXPORT CSV \"{}.dmx\"" .format(run_filename))
    apt_script.append("TRAC 0 CLOSE")
    apt_script.append("EXIT")

    return apt_script