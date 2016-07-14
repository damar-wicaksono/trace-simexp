"""Common module for paramfile package
"""

__author__ = "Damar Wicaksono"


def append_info(params_dict: list, info_filename: str):
    """Append the prepro.info with the list of parsed parameters

    :param params_dict: (list of dict) the parsed component parameters
    :param info_filename: (str) the filebane of prepro.info
    """

    with open(info_filename, "a") as info_file:
        for param in params_dict:
            info_file.writelines(param["str_msg"])


def var_type_str(var_type):
    if var_type == 1:
        return "additive"
    elif var_type == 2:
        return "substitutive"
    elif var_type == 3:
        return "multiplicative"


def parse_var_params(parlist_entry: str) -> dict:
    r"""Parse an entry of param_list file, grab the parameters of distribution

    :param parlist_entry: an entry (a line) in the param_list file
    :return: dictionary with the parameters of the distribution
    """
    import re 
    import ast

    var_params = re.search("[\[({](.*?)[})\]]", parlist_entry).group(1)
    var_params = ast.literal_eval("{{{}}}" .format(var_params))

    return var_params
