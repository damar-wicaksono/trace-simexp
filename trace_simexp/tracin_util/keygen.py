"""Module to generate key used in the trace input deck template"""


__author__ = "Damar Wicaksono"


def create(param_dict: dict, template: bool=False, index: int=None) -> str:
    r"""Create a key based on a given dictionary of perturbed parameter
    
    :param param_dict: the dictionary of perturbed parameter
    :template: boolean flag to decide whether to add $ character or not
    :index: integer for multiple values in table or array type variable
    :return: string of key used in the template
    """
    if index != None:
        # Multiple perturbed parameters
        key = "par_{:03d}_{:03d}" .format(param_dict["enum"], index)
        if template:
            key = "{{{}}}" .format(key) # Curly bracket to accomodate cont. sym
    else:
        key = "par_{:03d}" .format(param_dict["enum"])

    if template:
        # Add key flag if written for the template
        key = "$" + key

    return key
