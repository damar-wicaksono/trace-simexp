"""Module to parse list of parameters file and convert it into python dictionary
"""
from .parse_senscoef import parse_senscoef
from .parse_matprop import parse_matprop
from .parse_spacer import parse_spacer
from .parse_comp import parse_comp

__author__ = "Damar Wicaksono"


def inp_to_dict(param_list_file, verbose=True, comment_char="#"):
    r"""Read list of parameters file and create a python dictionary out of it

    :param param_list_file: (str) the fullname of list of parameters file
    :param verbose: (bool) terminal printing or not
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
                keyword = line.split()[1].lower()

                if keyword == "spacer":
                    # spacer grid data is specified, update params_dict
                    parse_spacer(line, params_dict, verbose)

                elif keyword == "matprop":
                    # material properties data is specified, update params_dict
                    parse_matprop(line, params_dict, verbose)

                elif keyword == "senscoef":
                    # sensitivity coefficient is specified, update params_dict
                    parse_senscoef(line, params_dict, verbose)

                elif keyword in components:
                    # component parameter is specified, update params_dict
                    parse_comp(line, params_dict, verbose)

                else:
                    raise NameError("*{}* data type is not supported!"
                                    .format(keyword))

    return params_dict


