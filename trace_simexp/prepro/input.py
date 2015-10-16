__author__ = "Damar Wicaksono"


def get():
    """

    :return:
    """
    from .input_parser import command_line_args

    inputs = dict()

    samples, base_dirname, tracin_base_fullname, \
    dm_fullname, params_list_fullname, overwrite = command_line_args.get()

    base_name = base_dirname.split("/")[-1]
    case_name = tracin_base_fullname.split("/")[-1].split(".")[0]
    dm_name = dm_fullname.split("/")[-1].split(".")[0]
    params_list_name = params_list_fullname.split("/")[-1].split(".")[0]

    inputs = {
        "samples": samples,
        "base_dir": base_dirname,
        "base_name": base_name,
        "tracin_base_file": tracin_base_fullname,
        "case_name": case_name,
        "dm_file": dm_fullname,
        "dm_name": dm_name,
        "params_list_file": params_list_fullname,
        "params_list_name": params_list_name,
        "overwrite": overwrite
    }

    print_info(inputs, "test.info")
    return inputs


def print_info(inputs, info_file):
    """

    :return:
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

    with open(info_file, "wt") as file:
        file.writelines("TRACE Simulation Experiment - Date: {}\n"
                        .format(str(datetime.now())))
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

        for i in range(int(len(inputs["samples"])/10)):
            offset1 = i*10
            offset2 = (i+1)*10
            for j in range(offset1, offset2 - 1):
                file.writelines(" {:5d} " .format(inputs["samples"][j]))
            file.writelines(" {:5d}\n" .format(inputs["samples"][offset2-1]))

        offset1 = int(len(inputs["samples"])/10) * 10
        offset2 = len(inputs["samples"])
        for i in range(offset1, offset2 - 1):
            file.writelines(" {:5d} " .format(inputs["samples"][i]))
        file.writelines(" {:5d}\n" .format(inputs["samples"][offset2-1]))
