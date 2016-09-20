"""Module to write down trace input deck based on sampled parameter values
"""

__author__ = "Damar Wicaksono"

COMPONENTS = ["pipe", "vessel", "power", "fill", "break"]


def create(template_lines, params_dict, norm_pert_factors):
    r"""Function to create a trace input as string based on perturbed values

    :param template_lines: (str.Template) the template based on base tracin
    :param params_dict: (list of dict) the list of parameters in a dictionary
    :param norm_pert_factors: (array) an array of normalized perturbed factor
    :return: (str) a tracin with template keys substituted with the actual
        perturbed model parameter values
    """
    from .tracin_util import perturb

    # A simple dimension checking
    if len(params_dict) != len(norm_pert_factors):
        raise ValueError("The # of sampled values and # of parameters unequal!")

    perturb_dict = dict()

    # Loop over all parameters in the list of dictionaries
    for i, param in enumerate(params_dict):

        # Rescale the pert_factors according to the params_dict
        rescaled_factor = perturb.rescale_perturb(param, norm_pert_factors[i])

        # Perturbed the model parameters
        perturb_param = perturb.perturb_param(param, rescaled_factor)

        # Create dictionary with keys correspond to template lines and perturbed
        # model parameter values
        perturb_dict.update(perturb.create_dict(param, perturb_param))

    # replace the key in template with perturbed values
    tracin = template_lines.substitute(perturb_dict)

    return tracin


def get_nominal_values(tracin_lines: list, params_dict: list):
    r"""Procedure to read base tracin and get nominal parameter values

    The procedure will update the param_dict with new key: ["nom_vals"].
    Depending on the ["var_type"] there can be a single value of nominal value
    (i.e., for scalar) or multiple values of it (i.e., table or array).

    :param tracin_lines: (list) the contents of the base tracin
    :param params_dict: (list of dict) list of parameters in dictionaries
    """
    from .template import tracin_spacer
    from .template import tracin_senscoef
    from .template import tracin_matprop
    from .template import tracin_comp

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


def create_template(params_dict: list, tracin_lines: list):
    r"""Procedure to create tracin template string

    The string contains `keys` to be substituted with values based on the
    design matrix.

    :param params_dict: (list) the list of parameters in the dictionary
    :param tracin_lines: (list) the contents of base case tracin file
    :returns: (str template) the template of tracin in string format
    """
    import string

    from .template import tracin_spacer
    from .template import tracin_senscoef
    from .template import tracin_comp
    from .template import tracin_matprop

    tracin_tmp_lines = tracin_lines
    # Loop over all specified parameters and replace the base tracin with key
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

