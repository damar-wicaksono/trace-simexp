# -*- coding: utf-8 -*-
"""
    trace_simexp.info_file.execute
    *******************************

    Module to parse and generate info file of post-processing phase
"""

__author__ = "Damar Wicaksono"


def read(exec_info_contents: list) -> tuple:
    """Read the exec info file produced in the execution phase

    :param exec_info_contents: the contents of the execute phase info file
    :return: A tuple with the following contents
        (str) the fullname of prepro info file
        (str) the base directory
        (str) the name of the base TRACE input deck, without extension
        (str) the name of the list of parameters file, without extension
        (str) the name of the design matrix file, without extension
        (str) the scratch directory
        (list, int) list of executed samples as reported in the exec info file
    """
    scratch_dir = None
    
    for num_line, line in enumerate(exec_info_contents):

        # The fullname of pre-process info file
        if "prepro.info File" in line:
            prepro_info_fullname = line.split("-> ")[-1].strip()
        # The base directory
        if "Base Directory Name" in line:
            base_dir = line.split("-> ")[-1].strip()
        # The base case name
        if "Base Case Name" in line:
            case_name = line.split("-> ")[-1].strip()
        # The list of parameters file name
        if "List of Parameters Name" in line:
            params_list_name = line.split("-> ")[-1].strip()
        # The design matrix file name
        if "Design Matrix Name" in line:
            dm_name = line.split("-> ")[-1].strip()
        # The scratch directory
        if "Scratch Directory Name" in line:
            scratch_dir = line.split("-> ")[-1].strip()
        # Executed samples
        if "Samples to Run" in line:
            samples = []
            i = num_line + 1
            while True:
                if "***  End of Samples  ***" in exec_info_contents[i]:
                    break
                samples.extend([int(_) for _ in exec_info_contents[i].split()])
                i += 1

    return (prepro_info_fullname, base_dir, case_name, params_list_name,
            dm_name, scratch_dir, samples)


def write(inputs: dict):
    """Write a summary of the execution phase (a.k.a exec.info)

    The exec.info serves as a log file for the command line arguments, the
    relevant info taken from the prepro.info. The file will also serves as a
    link to the next phase

    :param inputs: (dict) the required inputs for execute phase in a dictionary
    :return: the exec.info file with the specified filename
    """
    from datetime import datetime
    from . import common

    header = ["prepro.info Name", "prepro.info File",
              "Base Directory Name", "Base Case Name",
              "List of Parameters Name", "Design Matrix Name",
              "TRACE Executable", "XTV2DMX Executable",
              "Scratch Directory Name", "Number of Processors",
              "Samples to Run"]

    with open(inputs["info_file"], "wt") as info_file:
        info_file.writelines("TRACE Simulation Experiment - Date: {}\n"
                             .format(str(datetime.now())))

        # Info file header
        info_file.writelines("***Execute Phase Info***\n")

        # prepro.info filename
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[0], "->",
                                     inputs["prepro_info_name"]))
        # prepro.info fullname
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[1], "->",
                                     inputs["prepro_info_fullname"]))

        # base directory name
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[2], "->",
                                     inputs["base_dir"]))

        # base case name
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[3], "->",
                                     inputs["case_name"]))

        # list of parameters name
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[4], "->",
                                     inputs["params_list_name"]))

        # design matrix name
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[5], "->",
                                     inputs["dm_name"]))

        # TRACE Executable
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[6], "->", inputs["trace_exec"]))

        # XTV2DMX Executable
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[7], "->", inputs["xtv2dmx_exec"]))

        # Scratch Directory Name
        if inputs["scratch_dir"] is not None:
            info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                                 .format(header[8], "->",
                                         inputs["scratch_dir"]))

        # Number of Processors and hostname
        info_file.writelines("{:<30s}{:3s}{:<3d}({})\n"
                             .format(header[9], "->", inputs["num_procs"],
                                     inputs["hostname"]))

        # Samples to Run
        info_file.writelines("{:<30s}{:3s}\n" .format(header[10], "->"))
        common.write_by_tens(inputs["samples"], "5d", info_file)
        # Mark the end of samples
        info_file.writelines("***  End of Samples  ***\n")
