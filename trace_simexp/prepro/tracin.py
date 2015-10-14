"""Module to write down trace input deck based on sampled parameter values
"""

__author__ = "Damar Wicaksono"


def create(template_lines, params_dict, norm_pert_factors):
    r"""Function to create a trace input as string based on perturbed values

    :param template_lines: (str.Template) the template based on base tracin
    :param params_dict: (list of dict) the list of parameters in a dictionary
    :param norm_pert_factors: (array) an array of normalized perturbed factor
    :return: (str) a tracin with template keys substituted with the actual
        perturbed model parameter values
    """
    from .tracin_generator import perturb

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
