"""Main module for post-processing activities - Post-processing Phase
"""
__author__ = "Damar Wicaksono"


def dmx2csv(postpro_inputs: dict, trace_vars: str):
    """Driver function to convert the dmx or xtv file into a csv file
    """
    from .pkg_postpro import dmx2csv
    from .util import create_iter

    num_samples = len(postpro_inputs["samples"])
    case_name = postpro_inputs["case_name"]

    for batch_iter in create_iter(num_samples, postpro_inputs["num_procs"]):

        # Put the iterator from create_iter into a list for re-usage
        # Use the samples instead of bare iterator
        return None


def get_input():
    """Get the inputs

    :return:
    """
    from .pkg_postpro import input
    from .pkg_postpro import info_file

    postpro_inputs = dict()

    #vars = input.read_tracevars("./simulation/xtvVars.inp")

    # Get command line arguments
    exec_infofile, trace_vars, aptplot_exec = input.get_args()

    # Read exec.info file

    # Read prepro.info file

    # Read the list of TRACE variables name

    # Combine all parameters in a python dictionary
    postpro_inputs = {"exec_info": exec_infofile,
                      "trace_vars_file": trace_vars,
                      "aptplot_exec": aptplot_exec}

    return postpro_inputs
