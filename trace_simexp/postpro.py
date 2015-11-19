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
    from .pkg_execute import input_parser

    postpro_inputs = dict()

    # Get command line arguments
    exec_infofile, trace_vars_file, aptplot_exec, num_procs = input.get_args()

    # Read exec.info file
    prepo_infofile, samples = info_file.exec_read(exec_infofile)

    # Read prepro.info file
    base_dir, case_name, params_list_name, dm_name, avail_samples = \
        input_parser.info_file.prepro_read(prepo_infofile)

    # Read the list of TRACE variables name
    trace_vars = input.read_tracevars(trace_vars_file)

    # Combine all parameters in a python dictionary
    postpro_inputs = {"exec_info": exec_infofile,
                      "trace_vars_file": trace_vars,
                      "aptplot_exec": aptplot_exec,
                      "num_procs": num_procs,
                      "samples": samples,
                      "trace_vars": trace_vars,
                      "prepro_info": prepo_infofile,
                      "base_dir": base_dir,
                      "case_name": case_name,
                      "params_list_name": params_list_name,
                      "dm_name": dm_name,
                      }

    return postpro_inputs
