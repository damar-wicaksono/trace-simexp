# -*- coding: utf-8 -*-
"""
    trace_simexp.paramfile.common
    *****************************

    Module with common functions to be used across modules within paramfile
    package
"""

__author__ = "Damar Wicaksono"


def append_info(params_dict: list, info_filename: str):
    """Append the prepro.info with the list of parsed parameters

    :param params_dict: the parsed component parameters as list of dictionary
    :param info_filename: the filename of prepro.info
    """

    with open(info_filename, "a") as info_file:
        for param in params_dict:
            info_file.writelines(param["str_msg"])


def var_type_str(var_type: int) -> str:
    """The name of the mode of perturbation

    :param var_type: the mode of variation as integer
    :return: the name of the mode of perturbation as string
    """
    if var_type == 1:
        return "substitutive"
    elif var_type == 2:
        return "additive"
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


def print_var_params(var_params: dict) -> str:
    r"""Print the parsed var_params in the message"""
    str_msg = list()

    for key, value in var_params.items():
        str_msg.append(" - {}: {}" .format(key, value))
    
    return "\n".join(str_msg)
