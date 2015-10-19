"""Module to write info file from parsing the command line
"""

__author__ = "Damar Wicaksono"


def write(inputs, info_filename):
    r"""Write the command line arguments into a file

    :param inputs: (dict) the command line arguments as dictionary
    :param info_filename: (str) the filename of the info_file
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

    with open(info_filename, "wt") as file:
        file.writelines("TRACE Simulation Experiment - Date: {}\n"
                        .format(str(datetime.now())))
        file.writelines("{}\n" .format(inputs["info"]))
        file.writelines("***Preprocessing Phase Info***\n")
        file.writelines("{:<30s}{:3s}{:<30s}\n"
                        .format(header[0], "->", inputs["base_name"]))
        file.writelines("{:<30s}{:3s}{:<30s}\n"
                        .format(header[1], "->", inputs["base_dir"]))
        file.writelines("{:<30s}{:3s}{:<30s}\n"
                        .format(header[2], "->", inputs["case_name"]))
        file.writelines("{:<30s}{:3s}{:<30s}\n"
                        .format(header[3], "->", inputs["tracin_base_file"]))
        file.writelines("{:<30s}{:3s}{:<30s}\n"
                        .format(header[4], "->", inputs["params_list_name"]))
        file.writelines("{:<30s}{:3s}{:<30s}\n"
                        .format(header[5], "->", inputs["params_list_file"]))
        file.writelines("{:<30s}{:3s}{:<30s}\n"
                        .format(header[6], "->", inputs["dm_name"]))
        file.writelines("{:<30s}{:3s}{:<30s}\n"
                        .format(header[7], "->", inputs["dm_file"]))
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


def make_filename(inputs_dict):
    r"""Create a string of filename for the file_info based on the inputs

    The function is called by default, if no custom filename is specified

    :param inputs_dict: (dict) the command line arguments as dictionary
    :return: (str) the info_filename as string
    """

    if len(inputs_dict["samples"]) > 1:
        info_file = "info-{}-{}-{}-{}-{}.txt" \
            .format(inputs_dict["case_name"],
                    inputs_dict["params_list_name"],
                    inputs_dict["dm_name"],
                    inputs_dict["samples"][0],
                    inputs_dict["samples"][-1])
    else:
        info_file = "info-{}-{}-{}-{}" \
            .format(inputs_dict["case_name"],
                    inputs_dict["params_list_name"],
                    inputs_dict["dm_name"],
                    inputs_dict["samples"][0])

    return info_file
