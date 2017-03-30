# -*- coding: utf-8 -*-
"""
    trace_simexp.info_file.postpro
    ******************************

    Module to parse and generate info file of post-processing phase
"""

__author__ = "Damar Wicaksono"


def read(postpro_info_contents: list) -> tuple:
    """Parse the info file produced in the post-processing phase
    
    :param postpro_info_contents: the contents of the post-process phase info
    :return: a tuple with the following contents
        (str) the fullname of execute info file
        (str) the base directory
        (str) the name of the base TRACE input deck, sans extension
        (str) the name of the list of parameters file, sans extension
        (str) the name of the design matrix file, sans extension
        (str) the name of the list of TRACE graphic variables file, sans ext.
        (list, int) the post-processed samples
    """
    # Loop over lines to obtain the parameters
    for num_line, line in enumerate(postpro_info_contents):

        # Execute Info File
        if "exec.info File" in line:
            exec_info_fullname = line.split("-> ")[-1].strip()
        # The base directory name
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
        # The list of TRACE graphic variables name
        if "List of XTV Variables Name" in line:
            xtv_vars_name = line.split("-> ")[-1].strip()
        # Post-processed samples
        if "Samples to Post-process" in line:
            samples = []
            i = num_line + 1
            while True:
                if "***  End of Samples  ***" in postpro_info_contents[i]:
                    break
                samples.extend(
                    [int(_) for _ in postpro_info_contents[i].split()])
                i += 1

    return (exec_info_fullname, base_dir, case_name, params_list_name,
            dm_name, xtv_vars_name, samples)


def write(inputs: dict):
    """Write a summary of the post-processing phase (a.k.a postpro.info)

    :param inputs: (dict) the required inputs for post-pro phase in a dictionary
    """
    from datetime import datetime
    from . import common

    header = ["exec.info Name", "exec.info File",
              "Base Directory Name", "Base Case Name",
              "List of Parameters Name", "Design Matrix Name",
              "APTPlot Executable", "Number of Processors (Host)",
              "List of XTV Variables Name", "List of XTV Variables File", 
              "List of XTV Variables", "Samples to Post-process"]

    with open(inputs["info_file"], "wt") as info_file:

        # Print the header
        info_file.writelines("TRACE Simulation Experiment - Date: {}\n"
                             .format(str(datetime.now())))

        # Info file header
        info_file.writelines("***Post-process Phase Info***\n")

        # exec.info filename
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[0], "->",
                                     inputs["exec_info_name"]))

        # exec.info fullname
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[1], "->",
                                     inputs["exec_info_fullname"]))

        # Base directory fullname
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[2], "->",
                                     inputs["base_dir"]))

        # Base case name
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[3], "->",
                                     inputs["case_name"]))

        # List of parameters name
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[4], "->",
                                     inputs["params_list_name"]))

        # Design matrix name
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[5], "->",
                                     inputs["dm_name"]))

        # APTPlot Executable
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[6], "->", inputs["aptplot_exec"]))

        # Number of Processors and hostname
        info_file.writelines("{:<30s}{:3s}{:<3d}({})\n"
                             .format(header[7], "->",
                                     inputs["num_procs"],
                                     inputs["hostname"]))

        # List of Graphic Variables Name
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[8], "->",
                                     inputs["xtv_vars_name"]))

        # List of Graphic Variables File
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[9], "->",
                                     inputs["xtv_vars_fullname"]))

        # List of Graphic Variables
        info_file.writelines("{:<30s}{:3s}\n" .format(header[10], "->"))
        common.write_by_tens(inputs["xtv_vars"], ">20s", info_file)

        # Samples to post-processed
        info_file.writelines("{:<30s}{:3s}\n" .format(header[11], "->"))
        common.write_by_tens(inputs["samples"], "5d", info_file)
        # Mark the end of samples
        info_file.writelines("***  End of Samples  ***\n")
