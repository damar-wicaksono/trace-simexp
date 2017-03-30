# -*- coding: utf-8 -*-
"""
    trace_simexp.reset
    ******************

    Main module to reset selected phases
"""

__author__ = "Damar Wicaksono"


def get_input() -> dict:
    """Get the command line arguments, read the info file, and construct dict

    :return: All the inputs used for resetting a phase as dictionary
    """
    from . import cmdln_args
    from .info_file import common, prepro, execute, postpro

    info_file_contents = cmdln_args.reset.get()          # get the contents
    phase = common.sniff_info_file(info_file_contents)   # decide the type

    # Consolidate into a dictionary
    reset_inputs = {
        "phase": phase
    }

    # Read the preprocess file according to their type
    if phase == "prepro":
        # Read the pre-processing phase info file
        reset_inputs["base_dir"], reset_inputs["case_name"], \
            reset_inputs["params_list_name"], reset_inputs["dm_name"], \
            reset_inputs["samples"] = prepro.read(info_file_contents)
    elif phase == "exec":
        # Read the execute phase info file
        reset_inputs["prepro_info_fullname"], reset_inputs["base_dir"],\
            reset_inputs["case_name"], reset_inputs["params_list_name"], \
            reset_inputs["dm_name"], reset_inputs["scratch_dir"],\
            reset_inputs["samples"] = execute.read(info_file_contents)

    elif phase == "postpro":
        # Read the post-processing phase info file
        reset_inputs["exec_info_fullname"], reset_inputs["base_dir"], \
            reset_inputs["case_name"], reset_inputs["params_list_name"], \
            reset_inputs["dm_name"], reset_inputs["xtv_vars_name"], \
            reset_inputs["samples"] = postpro.read(info_file_contents)

    return reset_inputs
