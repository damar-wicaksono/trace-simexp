"""Module to write down trace input deck based on sampled parameter values
"""

__author__ = "Damar Wicaksono"


def create(template_lines, params_dict, normalized_pert_values):
    r"""Function to create a trace input as string based on perturbed values

    :param template_lines:
    :param params_dict:
    :param normalized_pert_values:
    :return:
    """

    # Rescale the pert_values according to the params_dict
    # Create dictionary with keys correspond to template lines and values from
    # rescaled perturbed values
    # replace the key in template with perturbed values
    # return the perturbed tracin string
    # done

    realization = dict()

    for i, param in enumerate(params_dict):
        scaled_value(param, normalized_pert_values[i])

    tracin = template_lines.substitute(realization)
    return tracin


