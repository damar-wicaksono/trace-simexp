"""Module to parse list of parameters file and convert it into python dictionary
"""

__author__ = "Damar Wicaksono"


def inp_to_dict(param_list_file, verbose=True, comment_char="#"):
    r"""Read list of parameters file and create a python dictionary out of it

    :param param_list_file: (str) the fullname of list of parameters file
    :param verbose: (bool) terminal printing or not
    :param comment_char: (str) the character signifying comment line in the file
    :returns: (list of dict) the parameter perturbation specification in a list
        of dictionary
    """

    # Open and read list of parameters file
    with open(param_list_file, "rt") as params_file:
        for line in params_file.readlines():
            if not line.startswith(comment_char):
                print(line.strip())


def parse_senscoef(line, params_dict, verbose=True):
    r"""Parse sensitivity coefficient specification from list of parameters file

    note that the input argument `params_dict` is mutable and will be modified

    :param line: (list of str) a line read from list of parameters file
    :param params_dict: (list of dict) the list of parameters in a dictionary
    :param verbose: (bool) terminal printing or not
    :returns: (list of dict) an updated params_dict with senscoef specification
    """
    pass


def parse_spacer(line, params_dict, verbose=True):
    r"""Parse spacer grid specification from a list of parameters file

    note that the input argument `params_dict` is mutable and will be modified

    :param line: (list of str) a line read from list of parameters file
    :param params_dict: (list of dict) the list of parameters in a dictionary
    :param verbose: (bool) terminal printing or not
    :returns: (list of dict) an updated params_dict with spacer specification
    """
    pass


def parse_matprop(line, params_dict, verbose=True):
    r"""Parse material property specification from a list of parameters file

    note that the input argument `params_dict` is mutable and will be modified

    :param line: (list of str) a line read from list of parameters file
    :param params_dict: (list of dict) the list of parameters in a dictionary
    :param verbose: (bool) terminal printing or not
    :returns: (list of dict) an updated params_dict with matprop specification
    """
    pass


def parse_comp(line, params_dict, verbose=True):
    r"""Parse component parameter specification from a list of parameters file

    note that the input argument `params_dict` is mutable and will be modified

    :param line: (list of str) a line read from list of parameters file
    :param params_dict: (list of dict) the list of parameters in a dictionary
    :param verbose: (bool) terminal printing or not
    :returns: (list of dict) an updated params_dict with comp specification
    """
    pass