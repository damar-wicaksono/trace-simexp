"""Module to parse and generate info file in post-processing phase
"""

__author__ = "Damar Wicaksono"


def write(inputs: dict, info_filename: str):
    """Write a summary of the post-processing phase (a.k.a postpro.info)

    :param inputs: (dict) the required inputs for post-pro phase in a dictionary
    :param info_filename: (str) the filename of the postpro.info file
    """
    from datetime import datetime

    header = ["prepro.info Filename", "exec.info Filename",
              "APTPlot Executable", "Number of Processors (Host)",
              "List of XTV Variables Files", "List of XTV Variables",
              "Samples to Post-processed"]

    with open(info_filename, "wt") as info_file:

        # Print the header
        info_file.writelines("TRACE Simulation Experiment - Date: {}\n"
                             .format(str(datetime.now())))

        # Info file header
        info_file.writelines("***Post-process Phase Info***\n")

        # prepro.info filename
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[0], "->", inputs["prepro_info"]))

        # exec.info filename
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[1], "->", inputs["exec_info"]))

        # APTPlot Executable
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[2], "->", inputs["aptplot_exec"]))

        # Number of Processors and hostname
        info_file.writelines("{:<30s}{:3s}{:<3d}({})\n"
                             .format(header[3], "->", inputs["num_procs"],
                                     inputs["hostname"]))

        # List of Graphic Variables Files
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[4], "->",
                                     inputs["xtv_vars_file"]))

        # List of Graphic Variables
        info_file.writelines("{:<30s}{:3s}\n" .format(header[5], "->"))

        for i in range(int(len(inputs["xtv_vars"])/3)):
            offset1 = i*3
            offset2 = (i+1)*3
            for j in range(offset1, offset2 - 1):
                info_file.writelines(" {:>20s} "
                                     .format(inputs["xtv_vars"][j]))
            info_file.writelines(" {:>20s}\n"
                                 .format(inputs["xtv_vars"][offset2-1]))

        offset1 = int(len(inputs["xtv_vars"])/3) * 3
        offset2 = len(inputs["xtv_vars"])
        if offset2 > offset1:
            for i in range(offset1, offset2):
                info_file.writelines(" {:>20s} "
                                     .format(inputs["xtv_vars"][i]))
            info_file.writelines("\n")

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