__author__ = "Damar Wicaksono"


def get():
    """

    :return:
    """
    import numpy as np
    from .input_parser import command_line_args

    inputs = dict()

    samples, base_dirname, tracin_base_fullname, \
    dm_fullname, params_list_fullname, overwrite, info = command_line_args.get()

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
        "overwrite": overwrite,
        "info": info
    }

    # Check the validity of the inputs
    check_inputs(inputs)

    # Update samples if all samples are asked
    if isinstance(inputs["samples"], bool) and inputs["samples"]:
        num_samples = np.loadtxt(inputs["dm_file"]).shape[0]
        inputs["samples"] = list(range(1, num_samples+1))

    # Write to a file the summary of report
    print_inputs(inputs, "test.info")
    return inputs


def print_inputs(inputs, info_file):
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
        for i in range(offset1, offset2 - 1):
            file.writelines(" {:5d} " .format(inputs["samples"][i]))
        file.writelines(" {:5d}\n" .format(inputs["samples"][offset2-1]))


def check_inputs(inputs):
    """

    :param inputs:
    :return:
    """
    import os
    import numpy as np

    # Check if the base tracin exists
    if not os.path.exists(inputs["tracin_base_file"]):
        raise ValueError("The base tracin file does not exist!")
    else:
        pass

    # Check if design matrix file exist
    if os.path.exists(inputs["dm_file"]):
        num_params_dm = np.loadtxt(inputs["dm_file"]).shape[1]
        num_samples = np.loadtxt(inputs["dm_file"]).shape[0]
    else:
        raise ValueError("The design matrix file does not exists!")

    # Check if list of parameters file exist
    if os.path.exists(inputs["params_list_file"]):
        with open(inputs["params_list_file"], "rt") as params_list_file:
            params_list_line = params_list_file.readlines()
        num_params_list_file = 0
        for i in params_list_line:
            if not i.startswith("#"):
                num_params_list_file += 1
    else:
        raise ValueError("The list of parameters file does not exist!")

    # Check the number of parameters in the design matrix and list of parameters
    if num_params_list_file != num_params_dm:
        raise ValueError("The number of parameters is inconsistent\n"
                         "{:10d} in {} and {:10d} in {}"
                         .format(num_params_list_file,
                                 inputs["params_list_name"],
                                 num_params_dm,
                                 inputs["dm_name"]))
    else:
        pass

    # Check if the sample number asked is available
    if not isinstance(inputs["samples"], bool):
        if max(inputs["samples"]) > num_samples:
            raise ValueError("The sample asked is beyond the available "
                             "samples\n {:10d} asked and {:10d} in {}"
                         .format(max(inputs["samples"]),
                                 num_samples,
                                 inputs["dm_name"]))
    else:
        pass