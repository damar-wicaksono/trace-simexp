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


def make_apt(run_filename: str, xtv_vars_name: str,
             xtv_vars: list, xtv_ext="dmx") -> list:
    """Function to create an aptplot input file according to the requested vars

    The aptscript will extract listed TRACE graphic variables and write them to
    a csv file named:
        "{}-{}.csv" .format(run_filename, xtv_vars_filename)
    examples:
        run_filename = "febaTrans216-run_1"
        xtv_vars_filename = "xtvVars"
        csv_filename = "febaTrans216-run_1-xtvVars.csv"

    :param run_filename: the run name, case_name + sample_num
    :param xtv_vars_name: the name of the xtv variables list file
    :param xtv_vars: the list of TRACE graphic variables
    :param xtv_ext: the extension of the TRACE output, dmx or xtv
    :return: a list of string of aptplot command in batch mode
    """
    apt_script = list()

    apt_script.append("TRAC 0 XTV \"{}.{}\"" .format(run_filename, xtv_ext))

    # Write all the requested TRACE graphic variables
    for xtv_var in xtv_vars:
        apt_script.append("TREAD 0 \"{}\" SIU" .format(xtv_var))

    # Make the filename
    csv_filename = "{}-{}.csv" .format(run_filename, xtv_vars_name)

    apt_script.append("TRAC 0 EXPORT CSV \"{}\"" .format(csv_filename))
    apt_script.append("TRAC 0 CLOSE")
    apt_script.append("EXIT")

    return apt_script

