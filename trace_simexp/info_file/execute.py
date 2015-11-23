"""Module to parse and generate info file in post-processing phase
"""

__author__ = "Damar Wicaksono"


def read(info_filename: str):
    """Read the exec.info file produced in the execution phase

    :param info_filename: (str) the fullname of the exec.info file
    """

    # Read file
    with open(info_filename, "rt") as info_file:
        info_lines = info_file.read().splitlines()

    for num_line, line in enumerate(info_lines):

        if "prepro.info Filename" in line:
            prepro_info = line.split("-> ")[-1].strip()

        # Samples to run
        if "Samples to Run" in line:
            samples = []
            i = num_line + 1
            while True:
                if "***" in info_lines[i]:
                    break
                samples.extend([int(_) for _ in info_lines[i].split()])
                i += 1

    return prepro_info, samples


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
                             .format(header[0], "->", inputs["prepro_info"]))

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
