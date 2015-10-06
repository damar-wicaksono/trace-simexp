"""Module to create a tracin template file based on base case tracin and list of
parameters file
"""
from .paramfile import inp_to_dict

__author__ = "Damar Wicaksono"


def create(param_list_file, tracin_base_file, tracin_temp_file):
    r"""Procedure to create tracin template file

    :param param_list_file: (str) the fullname of list of parameters file
    :param tracin_base_file: (str) the fullname of base case tracin file
    :param tracin_temp_file: (str) the fullname of template tracin file to be
        produced
    """
    params_dict = inp_to_dict(param_list_file, verbose=False)


def get_nominal_values(tracin_file, params_dict):
    r"""Procedure to read base tracin and get nominal parameter values

    The procedure will update the param_dict with new key: ["nom_vals"].
    Depending on the ["var_type"] there can be a single value of nominal value
    (i.e., for scalar) or multiple values of it (i.e., table or array).

    :parameter tracin_file: (str) the fullname of the base tracin
    :parameter params_dict: (list of dict) list of parameters in dictionaries
    """
    # Read file and put the lines into python list (and strip them directly)
    with open(tracin_file, "rt") as tracin:
        tracin_lines = tracin.read().splitlines()

    # Loop over line
    for tracin_line in tracin_lines:
        print(tracin_line)

    # if keyword is found, call data-type-specific parser to update the dicts