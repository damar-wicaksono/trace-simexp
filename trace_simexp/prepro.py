"""Main module for pre-processing activities - Pre-processing Phase
"""

__author__ = "Damar Wicaksono"


def get_input(info_filename: str) -> dict:
    """Get all the inputs for pre-processing phase

    Sources of inputs are: command line arguments, list of parameters file,
    trace base input, and design matrix file

    :param info_filename: the string of prepro.info file
    :return: All the inputs required for pre-processing phase in a dictionary
    """
    return None


def create_dirtree(prepro_inputs: dict):
    """Create a directory structure for the simulation campaign

    :param prepro_inputs: All the inputs required for pre-pro in a dictionary
    """
    return None


def reset(postpro_inputs: dict):
    """Delete the created directory structures according to the parameters

    :param prepro_inputs: (dict) the input parameters for pre-processing phase
    """
    return None
