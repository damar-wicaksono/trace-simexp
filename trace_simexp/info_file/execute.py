"""Module to parse and generate info file in post-processing phase
"""

__author__ = "Damar Wicaksono"


def read(exec_info_contents: list):
    """Read the exec info file produced in the execution phase

    :param exec_info_contents: (str) the fullname of the exec.info file
    :return: (str) the fullname of prepro info file
        (int) the number of samples in the exec info file
    """
    for num_line, line in enumerate(exec_info_contents):

        if "prepro.info Fullname" in line:
            prepro_info = line.split("-> ")[-1].strip()

        # Samples to run
        if "Samples to Run" in line:
            samples = []
            i = num_line + 1
            while True:
                if "***" in exec_info_contents[i]:
                    break
                samples.extend([int(_) for _ in exec_info_contents[i].split()])
                i += 1

    return prepro_info, samples


def write(inputs: dict):
    """Write a summary of the execution phase (a.k.a exec.info)

    The exec.info serves as a log file for the command line arguments, the
    relevant info taken from the prepro.info. The file will also serves as a
    link to the next phase

    :param inputs: (dict) the required inputs for execute phase in a dictionary
    :return: the exec.info file with the specified filename
    """
    from datetime import datetime

    header = ["prepro.info Name", "prepro.info Fullname",
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

        # TRACE Executable
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[2], "->", inputs["trace_exec"]))

        # XTV2DMX Executable
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[3], "->", inputs["xtv2dmx_exec"]))

        # Scratch Directory Name
        if inputs["scratch_dir"] is not None:
            info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                                 .format(header[4], "->",
                                         inputs["scratch_dir"]))

        # Number of Processors and hostname
        info_file.writelines("{:<30s}{:3s}{:<3d}({})\n"
                             .format(header[5], "->", inputs["num_procs"],
                                     inputs["hostname"]))

        # Samples to Run
        info_file.writelines("{:<30s}{:3s}\n" .format(header[6], "->"))

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

        # Info file header
        info_file.writelines("***  End of Samples  ***\n")
