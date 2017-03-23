"""Module to parse and generate info file in post-processing phase
"""

__author__ = "Damar Wicaksono"


def read(info_fullname: str):
    """Read the info file produced in the post-processing phase
    
    :param info_fullname: the fullname of the post-pro info file
    :return: (str) the run directory name
        (str) the name of the aptscript
    """
    from . import prepro
    
    # Read file
    with open(info_fullname, "rt") as info_file:
        info_lines = info_file.read().splitlines()
        
    # Loop over lines to obtain the parameters
    for num_line, line in enumerate(info_lines):
        
        # Prepro Info File 
        if "prepro.info Name" in line:
            prepro_info = line.split("-> ")[-1].strip()

        # Execute Info File
        if "exec.info Name" in line:
            exec_info = line.split("-> ")[-1].strip()
            
        # The name of aptplot script
        if "List of XTV Variables Files" in line:
            apt_name = line.split("-> ")[-1].strip()
            apt_name = apt_name.split("/")[-1]
            apt_name = apt_name.split(".")[0]
   
    return prepro_info, exec_info, apt_name
    
    
def write(inputs: dict):
    """Write a summary of the post-processing phase (a.k.a postpro.info)

    :param inputs: (dict) the required inputs for post-pro phase in a dictionary
    """
    from datetime import datetime

    header = ["prepro.info Name", "exec.info Name",
              "APTPlot Executable", "Number of Processors (Host)",
              "List of XTV Variables Name", "List of XTV Variables File", 
              "List of XTV Variables", "Samples to Post-processed"]

    with open(inputs["info_file"], "wt") as info_file:

        # Print the header
        info_file.writelines("TRACE Simulation Experiment - Date: {}\n"
                             .format(str(datetime.now())))

        # Info file header
        info_file.writelines("***Post-process Phase Info***\n")

        # prepro.info filename
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[0], "->",
                                     inputs["prepro_info_name"]))

        # exec.info filename
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[1], "->",
                                     inputs["exec_info_name"]))

        # APTPlot Executable
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[2], "->", inputs["aptplot_exec"]))

        # Number of Processors and hostname
        info_file.writelines("{:<30s}{:3s}{:<3d}({})\n"
                             .format(header[3], "->",
                                     inputs["num_procs"],
                                     inputs["hostname"]))

        # List of Graphic Variables Name
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[4], "->",
                                     inputs["xtv_vars_name"]))

        # List of Graphic Variables File
        info_file.writelines("{:<30s}{:3s}{:<30s}\n"
                             .format(header[5], "->",
                                     inputs["xtv_vars_fullname"]))

        # List of Graphic Variables
        info_file.writelines("{:<30s}{:3s}\n" .format(header[6], "->"))

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
        info_file.writelines("{:<30s}{:3s}\n" .format(header[7], "->"))

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

        info_file.writelines("***  End of Samples  ***\n")
