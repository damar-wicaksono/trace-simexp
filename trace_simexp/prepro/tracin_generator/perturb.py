"""Module to perturb model parameters according to the sampled factors
"""

__author__ = "Damar Wicaksono"


def rescale_perturb(param_dict, norm_value):
    r"""Rescale the perturbation factor according to the specified distribution

    The perturbation factor is taken from a design matrix normalized between
    0 to 1. The function will rescale this factor according to the distribution
    specified in the dictionary.

    :param param_dict: (dict) the parameter dictionary
    :param norm_value: (float) the normalized [0,1] perturbation factor
    :returns: the rescaled value of the perturbation factor
    """
    pass


def perturb_param(param_dict, scaled_val):
    r"""Perturb the model parameter according to the mode of perturbation

    The function will perturb the nominal value of model parameter with the
    scaled value of perturbation factor according to the specified mode of
    variation. There are 3 available modes of perturbation:
        1. `1`: Additive perturbation
        2. `2`: Substitutive perturbation
        3. `3`: Multiplicative perturbation

    :param param_dict: (dict) the parameter dictionary
    :param scaled_val: (float or int) the scaled perturbation factor
    :returns: the perturbed parameter value
    """
    pass


def create_dict(param_dict, perturbed_param):
    r"""Create a key-value pair between template key and the perturbed parameter

    This key-value pair will be collected and use for substitution in the
    tracin template. The function will generate the key.

    :param param_dict: (dict) the parameter dictionary
    :param perturbed_param: (variant) the perturbed parameter value
    :returns: (dict) the key-value pair
    """
    pass