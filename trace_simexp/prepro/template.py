"""Module to create a tracin template file based on base case tracin and list of
parameters file
"""
from .paramfile import inp_to_dict

__author__ = "Damar Wicaksono"

# List of supported components
COMPONENTS = ["pipe", "vessel", "power", "fill", "break"]


def create(params_dict: list, tracin_file: str):
    r"""Procedure to create tracin template string

    The string contains `keys` to be substituted with values based on the
    design matrix.

    :param params_dict: (list) the list of parameters in the dictionary
    :param tracin_file: (str) the fullname of base case tracin file
        produced
    :returns: (str template) the template of tracin in string format
    """
    import string

    from .template_parser import tracin_spacer
    from .template_parser import tracin_senscoef
    from .template_parser import tracin_comp
    from .template_parser import tracin_matprop

    # Read tracin base case file
    with open(tracin_file, "rt") as tracin:
        tracin_lines = tracin.read().splitlines()

    tracin_tmp_lines = tracin_lines
    # Do something here to make the template
    for num, param in enumerate(params_dict):

        if param["data_type"] == "spacer":
            # spacer specified, look for it in the tracin
            tracin_tmp_lines = tracin_spacer.put_key(tracin_tmp_lines, param)

        elif param["data_type"] == "matprop":
            # material property specified, look for it in the tracin
            tracin_tmp_lines = tracin_matprop.put_key(tracin_lines, param)

        if param["data_type"] == "senscoef":
            # spacer specified, look for it in the tracin
            tracin_tmp_lines = tracin_senscoef.put_key(tracin_tmp_lines, param)

        if param["data_type"] in COMPONENTS:
            # spacer specified, look for it in the tracin
            tracin_tmp_lines = tracin_comp.put_key(tracin_tmp_lines, param)

    # Join the list of strings again with newline
    tracin_tmp_lines = " \n".join(tracin_lines)

    return string.Template(tracin_tmp_lines)


def get_nominal_values(tracin_file: str, params_dict: list):
    r"""Procedure to read base tracin and get nominal parameter values

    The procedure will update the param_dict with new key: ["nom_vals"].
    Depending on the ["var_type"] there can be a single value of nominal value
    (i.e., for scalar) or multiple values of it (i.e., table or array).

    :param tracin_file: (str) the fullname of the base tracin
    :param params_dict: (list of dict) list of parameters in dictionaries
    """
    from .template_parser import tracin_spacer
    from .template_parser import tracin_senscoef
    from .template_parser import tracin_matprop
    from .template_parser import tracin_comp

    # Read file and put the lines into python list (and strip them directly)
    with open(tracin_file, "rt") as tracin:
        tracin_lines = tracin.read().splitlines()

    # Loop over all parameters specified in params_dict
    for num, param in enumerate(params_dict):

        if param["data_type"] == "spacer":
            # spacer specified, look for it in the tracin
            params_dict[num]["nom_val"] = tracin_spacer.get_nom_val(
                tracin_lines, param
            )

        elif param["data_type"] == "matprop":
            # material property specified, look for it in the tracin
            params_dict[num]["nom_val"] = tracin_matprop.get_nom_val(
                    tracin_lines, param
            )

        elif param["data_type"] == "senscoef":
            # sensitivity coefficient specified, look for it in the tracin
            params_dict[num]["nom_val"] = tracin_senscoef.get_nom_val(
                tracin_lines, param
            )

        # component parameters specified, look for it in the tracin
        elif param["data_type"] in COMPONENTS:
            params_dict[num]["nom_val"] = tracin_comp.get_nom_val(
                tracin_lines, param
            )

        else:
            raise TypeError("Not a recognized data type")