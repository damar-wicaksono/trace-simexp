# -*- coding: utf-8 -*-
"""
command_line.py: Module with collections of command line interfaces for
trace-simexp
"""


def prepro():
    """trace-simexp pre-processing step command line interface"""

    import sys
    import os

    from trace_simexp import prepro
    from trace_simexp import tracin

    # Construct a dictionary of required inputs from command line arguments, etc
    inputs = prepro.get_input()

    # Check if info file already exists
    if os.path.exists(inputs["info_file"]):
        if inputs["overwrite"]:
            pass
        else:
            sys.exit("Prepro info file exist, no overwrite option, exiting...")

    # Read list of parameters file and create a dictionary from it
    params_dict = prepro.read_params(inputs["params_list_contents"],
                                     inputs["info_file"],
                                     inputs["tracin_base_contents"])

    # Create a string template
    tracin_template = tracin.create_template(params_dict,
                                             inputs["tracin_base_contents"])

    # Create a directory structure based on the specified input
    tracin.create_dirtree(inputs, params_dict, tracin_template)


def execute():
    """trace-simexp execution step command line interface"""

    from trace_simexp import execute
    # Consolidate all the required inputs for post-processing phase
    exec_inputs = execute.get_input()

    # Commence the conversion
    execute.run_batches(exec_inputs)


def postpro():
    """trace-simexp post-processing step command line interface"""

    from trace_simexp import postpro

    # Consolidate all the required inputs for post-processing phase
    postpro_inputs = postpro.get_input()

    # Commence the conversion
    postpro.dmx2csv(postpro_inputs)