"""Module to parse list of parameters file and convert it into python dictionary
"""
from .paramfile_parser import parser_senscoef
from .paramfile_parser import parser_matprop
from .paramfile_parser import parser_spacer
from .paramfile_parser import parser_comp

__author__ = "Damar Wicaksono"


def inp_to_dict(param_list_file, info_filename=None, comment_char="#"):
    r"""Read list of parameters file and create a python dictionary out of it

    :param param_list_file: (str) the fullname of list of parameters file
    :param info_filename: (str) the filename string for info_file
    :param comment_char: (str) the character signifying comment line in the file
    :returns: (list of dict) the parameter perturbation specification in a list
        of dictionary
    """
    # the list of supported component type
    components = ["pipe", "vessel", "power", "fill", "break"]

    # the list of dictionary of parameters list
    params_dict = []

    # Open and read list of parameters file
    with open(param_list_file, "rt") as params_file:
        for line in params_file.readlines():
            if not line.startswith(comment_char):
                line = line.strip()
                # the keyword for data type is the second entry in each line
                keyword = line.split()[1].lower()

                if keyword == "spacer":
                    # spacer grid data is specified, update params_dict
                    parser_spacer.parse(line, params_dict, info_filename)

                elif keyword == "matprop":
                    # material properties data is specified, update params_dict
                    parser_matprop.parse(line, params_dict, info_filename)

                elif keyword == "senscoef":
                    # sensitivity coefficient is specified, update params_dict
                    parser_senscoef.parse(line, params_dict, info_filename)

                elif keyword in components:
                    # component parameter is specified, update params_dict
                    parser_comp.parse(line, params_dict, info_filename)

                else:
                    raise NameError("*{}* data type is not supported!"
                                    .format(keyword))

    return params_dict


