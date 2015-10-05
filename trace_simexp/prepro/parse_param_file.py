"""Module to parse list of parameters file and convert it into python dictionary
"""
from .parse_spacer import parse_spacer

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
                    raise NameError("*{}* component is not supported!"
                                    .format(keyword))

    return params_dict


def parse_senscoef(line, params_dict, verbose=True):
    r"""Parse sensitivity coefficient specification from list of parameters file

    note that the input argument `params_dict` is mutable and will be modified

    :param line: (list of str) a line read from list of parameters file
    :param params_dict: (list of dict) the list of parameters in a dictionary
    :param verbose: (bool) terminal printing or not
    :returns: (list of dict) an updated params_dict with senscoef specification
    """
    senscoef_data = line.split()
    senscoef_dict = {
        "data_type": "senscoef",
        "num": senscoef_data[2],
        "var_name": None,
        "var_type": senscoef_data[4],
        "var_card": None,
        "var_word": None,
        "var_dist": senscoef_data[7],
        "var_par1": float(senscoef_data[8]),
        "var_par2": float(senscoef_data[9])
    }
    params_dict.append(senscoef_dict)

    if verbose:
        print("***{:2d}***" .format(int(senscoef_data[0])))
        print("Sensitivity coefficients with ID *{}* is specified"
              .format(senscoef_dict["num"]))
        print("Parameter distribution is *{}*"
              .format(senscoef_dict["var_dist"]))
        print("1st distribution parameter: {:.3f}"
              .format(senscoef_dict["var_par1"]))
        print("2nd distribution parameter: {:.3f}"
              .format(senscoef_dict["var_par2"]))


def parse_matprop(line, params_dict, verbose=True):
    r"""Parse material property specification from a list of parameters file

    note that the input argument `params_dict` is mutable and will be modified

    :param line: (list of str) a line read from list of parameters file
    :param params_dict: (list of dict) the list of parameters in a dictionary
    :param verbose: (bool) terminal printing or not
    :returns: (list of dict) an updated params_dict with matprop specification
    """
    print(line)


def parse_comp(line, params_dict, verbose=True):
    r"""Parse component parameter specification from a list of parameters file

    note that the input argument `params_dict` is mutable and will be modified

    :param line: (list of str) a line read from list of parameters file
    :param params_dict: (list of dict) the list of parameters in a dictionary
    :param verbose: (bool) terminal printing or not
    :returns: (list of dict) an updated params_dict with comp specification
    """
    print(line)