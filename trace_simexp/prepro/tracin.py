"""Module to write down trace input deck based on sampled parameter values
"""

__author__ = "Damar Wicaksono"


def create(template_lines, params_dict, norm_pert_factors):
    r"""Function to create a trace input as string based on perturbed values

    :param template_lines:
    :param params_dict:
    :param norm_pert_factors:
    :return:
    """
    from .tracin_generator import perturb

    realization = dict()

    # Loop over all parameters in the list of dictionaries
    for i, param in enumerate(params_dict):

        # Rescale the pert_factors according to the params_dict
        rescaled_factor = perturb.rescale_perturb(param, norm_pert_factors[i])

        # Perturbed the model parameters


    # Create dictionary with keys correspond to template lines and values from
    # rescaled perturbed values
    # replace the key in template with perturbed values
    # return the perturbed tracin string
    # done

