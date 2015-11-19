"""Module to read pre-processing info file - Execute phase
"""

__author__ = "Damar Wicaksono"


def prepro_read(info_fullname: str):
    r"""Read the info file produced in the pre-processing phase

    :param info_fullname: (str) the fullname of the pre-pro info file
    :return:
    """

    # Read file
    with open(info_fullname, "rt") as info_file:
        info_lines = info_file.read().splitlines()

    # Loop over lines to obtain the parameter
    for num_line, line in enumerate(info_lines):

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
                if "***" in info_lines[i]:
                    break
                samples.extend([int(_) for _ in info_lines[i].split()])
                i += 1

    return base_dir, case_name, params_list_name, dm_name, samples


def write(inputs: dict, info_filename: str):
    """Write a summary of the execution phase (a.k.a exec.info)

    The exec.info serves as a log file for the command line arguments, the
    relevant info taken from the prepro.info. The file will also serves as a
    link to the next phase

    :param inputs: (dict) the required inputs for execute phase in a dictionary
    :param info_filename: (str) the filename of the exec.info file
    :return: the exec.info file with the specified filename
    """
    from datetime import datetime

    header = ["prepro.info Filename", "TRACE Executable", "XTV2DMX Executable",
              "Scratch Directory Name", "Number of Processors",
              "Samples to Run"]

    with open(info_filename, "wt") as info_file:
        info_file.writelines("TRACE Simulation Experiment - Date: {}\n"
                             .format(str(datetime.now())))

        # Info file header
        info_file.writelines("***Execute Phase Info***\n")

        # prepro.info filename
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[0], "->", inputs["info_file"]))

        # TRACE Executable
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[1], "->", inputs["trace_exec"]))

        # XTV2DMX Executable
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[2], "->", inputs["xtv2dmx_exec"]))

        # Scratch Directory Name
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[3], "->", inputs["scratch_dir"]))

        # Number of Processors and hostname
        info_file.writelines("{:<30s}{:3s}{:<3d}({})\n"
                             .format(header[4], "->", inputs["num_procs"],
                                     inputs["hostname"]))

        # Samples to Run
        info_file.writelines("{:<30s}{:3s}\n" .format(header[5], "->"))

        for i in range(int(len(inputs["samples"])/10)):
            offset1 = i*10
            offset2 = (i+1)*10
            for j in range(offset1, offset2 - 1):
                info_file.writelines(" {:5d} " .format(inputs["samples"][j]))
            info_file.writelines(" {:5d}\n"
                                 .format(inputs["samples"][offset2-1]))

        offset1 = int(len(inputs["samples"])/10) * 10
        offset2 = len(inputs["samples"])
        if offset2 > offset1:
            for i in range(offset1, offset2):
                info_file.writelines(" {:5d} " .format(inputs["samples"][i]))
            info_file.writelines("\n")


def make_filename(inputs: dict) -> str:
    """Create a string of filename for the exec.info

    The function is called by default, if no custom filename is specified

    :param inputs: (dict) the required inputs for execute phase in a dictionary
    :return: (str) the filename as string
    """

    if len(inputs["samples"]) > 1:
        info_file = "exec-{}-{}-{}-{}-{}.info" \
            .format(inputs["case_name"],
                    inputs["params_list_name"],
                    inputs["dm_name"],
                    inputs["samples"][0],
                    inputs["samples"][-1])
    else:
        info_file = "exec-{}-{}-{}-{}.info" \
            .format(inputs["case_name"],
                    inputs["params_list_name"],
                    inputs["dm_name"],
                    inputs["samples"][0])

    return info_file
