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
    from . import rescale

    # Create rescale values according to the specified distribution
    if param_dict["var_dist"] == "unif":
        value = rescale.uniform(norm_value,
                                param_dict["var_pars"]["min"],
                                param_dict["var_pars"]["max"])
    elif param_dict["var_dist"] == "logunif":
        value = rescale.loguniform(norm_value,
                                   param_dict["var_pars"]["min"],
                                   param_dict["var_pars"]["max"])

    elif param_dict["var_dist"] == "normal":
        value = rescale.normal(norm_value,
                               param_dict["var_pars"]["mu"],
                               param_dict["var_pars"]["sigma"])

    elif param_dict["var_dist"] == "discrete":
        value = rescale.discrete(norm_value, param_dict["var_pars"])

    else:
        raise TypeError("Distribution is not supported!")

    return value


def perturb_param(param_dict, scaled_val):
    r"""Perturb the model parameter according to the mode of perturbation

    The function will perturb the nominal value of model parameter with the
    scaled value of perturbation factor according to the specified mode of
    variation. There are 3 available modes of perturbation:
        1. `1`: Substitutive perturbation
        2. `2`: Additive perturbation
        3. `3`: Multiplicative perturbation

    :param param_dict: (dict) the parameter dictionary
    :param scaled_val: (float or int) the scaled perturbation factor
    :returns: (list of str) the perturbed parameter value written in string
    """
    import numpy as np

    # If the type is scalar, force it to be a 1D array
    if param_dict["var_type"] == "table":
        nom_val = np.array(param_dict["nom_val"])
    else:
        nom_val = np.array([param_dict["nom_val"]])

    # Perturb the nominal value according to the mode of perturbation
    var_mode = param_dict["var_mode"]
    if var_mode == 1:
        # Mode 1 - Substitutive
        pert_val = np.repeat(scaled_val, len(nom_val))

    elif param_dict["var_mode"] == 2:
        # Mode 2 - Additive
        pert_val = nom_val + scaled_val

    elif param_dict["var_mode"] == 3:
        # Mode 3 - Multiplicative
        pert_val = nom_val * scaled_val

    str_output = []
    # Write down the perturbed value
    for i in range(len(pert_val)):
        str_val = "%{}" .format(param_dict["str_fmt"])
        str_val = str_val % pert_val[i]
        str_output.append(str_val)

    return str_output


def create_dict(param_dict, perturbed_param):
    r"""Create a key-value pair between template key & the perturbed parameter

    This key-value pair will be collected and use for substitution in the
    tracin template. The function will generate this key and value pair for
    a given parameter dictionary.

    :param param_dict: (dict) the parameter dictionary
    :param perturbed_param: (variant) the perturbed parameter value
    :returns: (dict) the key-value pair
    """
    from . import keygen

    perturb_dict = dict()

    # Create key and return the key-value dictionary
    if param_dict["var_type"] == "scalar":
        key = keygen.create(param_dict, template=False, index=None)
        perturb_dict.update({key: perturbed_param[0]})

    elif param_dict["var_type"] == "table" or param_dict["var_type"] == "array":
        for i in range(len(perturbed_param)):
            key = keygen.create(param_dict, template=False, index=i)
            perturb_dict.update({key: perturbed_param[i]})

    elif param_dict["var_type"] == "fit":
        pass

    return perturb_dict
