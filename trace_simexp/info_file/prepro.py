"""Module to parse and generate info file in pre-processing phase
"""

__author__ = "Damar Wicaksono"


def write(inputs: dict):
    r"""Write a summary of the pre-processing phase

    The summary serves a log file for the command line arguments used in the
    pre-processing phase as well as a link to next phase (execution) to avoid
    redundancy.

    :param inputs: (dict) the command line arguments as dictionary
    :return: the info_file with the specified filename
    """
    from datetime import datetime

    header = ["Base Name",
              "Base Directory Name",
              "Base Case Name",
              "Base Case File",
              "List of Parameters Name",
              "List of Parameters File",
              "Design Matrix Name",
              "Design Matrix File",
              "Samples to Run",
              "Overwrite Directory"]

    with open(inputs["info_file"], "wt") as file:
        file.writelines("TRACE Simulation Experiment - Date: {}\n"
                        .format(str(datetime.now())))
        file.writelines("{}\n" .format(inputs["info"]))
        file.writelines("***Pre-process Phase Info***\n")
        file.writelines("{:<30s}{:3s}{:<30s}\n"
                        .format(header[0], "->", inputs["base_name"]))
        file.writelines("{:<30s}{:3s}{:<30s}\n"
                        .format(header[1], "->", inputs["base_dirname"]))
        file.writelines("{:<30s}{:3s}{:<30s}\n"
                        .format(header[2], "->", inputs["case_name"]))
        file.writelines("{:<30s}{:3s}{:<30s}\n"
                        .format(header[3], "->", inputs["tracin_base_fullname"]))
        file.writelines("{:<30s}{:3s}{:<30s}\n"
                        .format(header[4], "->", inputs["params_list_name"]))
        file.writelines("{:<30s}{:3s}{:<30s}\n"
                        .format(header[5], "->", inputs["params_list_fullname"]))
        file.writelines("{:<30s}{:3s}{:<30s}\n"
                        .format(header[6], "->", inputs["dm_name"]))
        file.writelines("{:<30s}{:3s}{:<30s}\n"
                        .format(header[7], "->", inputs["dm_fullname"]))
        file.writelines("{:<30s}{:3s}{:<30}\n"
                        .format(header[9], "->", inputs["overwrite"]))
        file.writelines("{:<30s}{:3s}\n" .format(header[8], "->"))

        # Write the requested sampled runs
        for i in range(int(len(inputs["samples"])/10)):
            offset1 = i*10
            offset2 = (i+1)*10
            for j in range(offset1, offset2 - 1):
                file.writelines(" {:5d} " .format(inputs["samples"][j]))
            file.writelines(" {:5d}\n" .format(inputs["samples"][offset2-1]))

        offset1 = int(len(inputs["samples"])/10) * 10
        offset2 = len(inputs["samples"])
        if offset2 > offset1:
            for i in range(offset1, offset2):
                file.writelines(" {:5d} " .format(inputs["samples"][i]))
            file.writelines("\n")


def read(prepro_info_contents: list):
    """Read the info file produced in the pre-processing phase

    :param prepro_info_contents: (list) the contents of the prepro info file
    :return: (str) the base directory name
        (str) the base case name
        (str) the list of parameters filename, without extension, without path
        (str) the design matrix filename, without extension, without path
        (list) the list of samples to run
    """
    # Loop over lines to obtain the parameter
    for num_line, line in enumerate(prepro_info_contents):

        # Base Directory
        if "Base Directory Name" in line:
            base_dir = line.split("-> ")[-1].strip()

        # Base Case Name
        if "Base Case Name" in line:
            case_name = line.split("-> ")[-1].strip()

        # List of parameters name
        if "List of Parameters Name" in line:
            params_list_name = line.split("-> ")[-1].strip()

        # Design Matrix filename
        if "Design Matrix Name" in line:
            dm_name = line.split("-> ")[-1].strip()

        # Samples to run
        if "Samples to Run" in line:
            samples = []
            i = num_line + 1
            while True:
                if "***" in prepro_info_contents[i]:
                    break
                samples.extend([int(_) for _ in prepro_info_contents[i].split()])
                i += 1

    return base_dir, case_name, params_list_name, dm_name, samples
