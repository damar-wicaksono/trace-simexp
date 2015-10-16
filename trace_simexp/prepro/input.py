__author__ = "Damar Wicaksono"


def get():
    """

    :return:
    """
    from .input_parser import command_line_args

    inputs = dict()

    samples, base_dirname, base_tracin_fullname, \
    design_matrix_fullname, param_list_fullname = command_line_args.get()

    base_name = base_dirname.split("/")[-1]
    case_name = base_tracin_fullname.split("/")[-1].split(".")[0]
    dm_name = design_matrix_fullname.split("/")[-1].split(".")[0]
    param_list_name = param_list_fullname.split("/")[-1].split(".")[0]

    inputs = {
        "samples": samples,
        "base_dir": base_dirname,
        "base_name": base_name,
        "base_tracin_file": base_tracin_fullname,
        "case_name": case_name,
        "design_matrix_file": design_matrix_fullname,
        "dm_name": dm_name,
        "param_list_file": param_list_fullname,
        "param_list_name": param_list_name
    }

    return inputs
