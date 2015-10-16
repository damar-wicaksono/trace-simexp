__author__ = "Damar Wicaksono"


def get():
    """

    :return:
    """
    from .input_parser import command_line_args

    inputs = dict()

    samples, base_dirname, tracin_base_fullname, \
    design_matrix_fullname, params_list_fullname = command_line_args.get()

    base_name = base_dirname.split("/")[-1]
    case_name = tracin_base_fullname.split("/")[-1].split(".")[0]
    dm_name = design_matrix_fullname.split("/")[-1].split(".")[0]
    params_list_name = params_list_fullname.split("/")[-1].split(".")[0]

    inputs = {
        "samples": samples,
        "base_dir": base_dirname,
        "base_name": base_name,
        "tracin_base_file": tracin_base_fullname,
        "case_name": case_name,
        "design_matrix_file": design_matrix_fullname,
        "dm_name": dm_name,
        "params_list_file": params_list_fullname,
        "params_list_name": params_list_name
    }

    return inputs
