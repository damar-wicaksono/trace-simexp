"""Module to create a rescaled design matrix based on normalized design matrix
and list of parameters file
"""
from .parse_param_file import inp_to_dict

__author__ = "Damar Wicaksono"


def create(param_list_file, design_matrix_infile, design_matrix_outfile):
    """Function to create rescaled design matrix from a normalized one

    :param param_list_file: (str) the fullname of list of variables file
    :param design_matrix_infile: (str) the fullname of normalized design matrix
    :param design_matrix_outfile: (str) the fullname of rescaled design matrix
    """
    pass