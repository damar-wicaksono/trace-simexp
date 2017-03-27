# -*- coding: utf-8 -*-
"""
    trace_simexp.info_file.common
    *****************************

    Common module for info_file package with support utilities
"""

__author__ = "Damar Wicaksono"


def make_filename(inputs: dict, flag: str) -> str:
    """Create a string of filename for the info file

    The function is called by default, if no custom filename is specified

    Generic filename:

    <phase>-<case_name>-<parlist>-<dm>-<samples>-<YYMMDD>-<HHMMSS>.nfo

    for postprocessing phase there is additional tag for the TRACE graphic
    variable file after the samples and before the date.

    :param inputs: the required inputs for execute phase in a dictionary
    :param flag: the info file flag: prepro, exec, or postpro
    :return: the filename as string
    """
    import time

    if len(inputs["samples"]) > 1:
        info_file = "{}-{}-{}-{}-{}_{}" \
            .format(flag,
                    inputs["case_name"],
                    inputs["params_list_name"],
                    inputs["dm_name"],
                    inputs["samples"][0],
                    inputs["samples"][-1])
    else:
        info_file = "{}-{}-{}-{}-{}" \
            .format(flag,
                    inputs["case_name"],
                    inputs["params_list_name"],
                    inputs["dm_name"],
                    inputs["samples"][0])

    # if postpro.info, additional id for list of graphic variable names
    if flag == "postpro":
        info_file = "{}-{}" .format(info_file, inputs["xtv_vars_name"])

    # Add date and time at the end
    today = time.strftime("%y%m%d")
    moment = time.strftime("%H%M%S")

    info_file = "{}-{}-{}.nfo" .format(info_file, today, moment)

    return info_file


def sniff_info_file(info_file_contents: list) -> str:
    """Sniff the contents of an info file to determine the phase of simulation

    :param info_file_contents: the contents of an info file
    :return: the info file type
    """
    if "***Pre-process Phase Info***" in info_file_contents:
        return "prepro"
    elif "***Execute Phase Info***" in info_file_contents:
        return "exec"
    elif "***Post-process Phase Info***" in info_file_contents:
        return "postpro"
    else:
        raise TypeError("Cannot determine which type of info file!")
