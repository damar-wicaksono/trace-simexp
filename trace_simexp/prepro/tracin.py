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
        realization.update(scaled_value(param, normalized_pert_values[i]))

    tracin = template_lines.substitute(realization)
    return tracin


def scaled_value(param_dict, normalized_value):
    """

    :param params_dict:
    :param normalized_pert_values:
    :return: (dict)
    """
    import numpy as np

    from .tracin_generator import rescale

    # Create rescale values
    if param_dict["var_dist"] == "unif":
        value = rescale.uniform(normalized_value,
                                param_dict["var_par1"],
                                param_dict["var_par2"])

    elif param_dict["var_dist"] == "logunif":
        value = rescale.loguniform(normalized_value,
                                   param_dict["var_par1"],
                                   param_dict["var_par2"])

    elif param_dict["var_dist"] == "normal":
        value = rescale.normal(normalized_value,
                               param_dict["var_par1"],
                               param_dict["var_par2"])

    elif param_dict["var_dist"] == "discunif":
        value = rescale.discunif(normalized_value, param_dict["var_par1"])

    else:
        raise TypeError("Distribution is not supported!")

    # Convert nominal values into numpy array
    nom_val = np.array(param_dict["nom_val"])

    # Perturb the nominal values
    if param_dict["var_mode"] == 1:
        # Mode 1 - Additive
        pert_value = nom_val + value

    elif param_dict["var_mode"] == 2:
        # Mode 2 - Substitutive
        pert_value = np.repeat(value, len(nom_val))

    elif param_dict["var_mode"] == 3:
        # Mode 3 - Multiplicative
        pert_value = nom_val * value

    # Create key and return the key-value dictionary
    if param_dict["var_type"] == "scalar":
        str_value = "%{}" .format(param_dict["str_fmt"])
        str_value = str_value % pert_value
        key = "{}_{}" .format(param_dict["data_type"], param_dict["enum"])
        return dict({key: str_value})

    elif param_dict["var_type"] == "table":
        pert_dict = dict()
        for i in range(len(pert_value)):
            str_value = "%{}" .format(param_dict["str_fmt"])
            str_value = str_value % pert_value[i]
            key = "{}_{}_{}" .format(param_dict["var_name"],
                                     param_dict["enum"],
                                     i)
            pert_dict.update({key: str_value})
        return(pert_dict)

    elif param_dict["var_type"] == "array":
        pass

    elif param_dict["var_type"] == "fit":
        pass

