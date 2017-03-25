# -*- coding: utf-8 -*-
"""
    trace_simexp.cmdln_interface
    ****************************

    Module with collections of command line interfaces for trace-simexp package
    to conduct simulation experiment using TRACE
"""
from ._version import __version__

def main():
    """Command line interface for echoing what is this all about"""
    print("trace-simexp version {}" .format(__version__))
    print("Conduct simulation experiment for TRACE")
    print("")
    print("Please use the driver scripts for each of the desired phases:")
    print("     trace_simexp_prepro     pre-process and generate perturbed "
          "inputs")
    print("     trace_simexp_execute    execute the generated perturbed " 
          "inputs")
    print("     trace_simexp_postpro    extract select variables from dmx")
    print("     trace_simexp_reset      return the original state of a given " 
          "phase")
    print("     trace_simexp_freeze     freeze current state for archival")
    print("Use <driver_script> --help to get the help for each")
    print("")


def cli_prepro():
    """Command line interface for trace-simexp pre-processing step"""

    from trace_simexp import prepro
    from trace_simexp import tracin
    from trace_simexp import info_file
    from trace_simexp import paramfile

    # Construct a dictionary of required inputs from command line arguments,etc
    inputs = prepro.get_input()

    # Write an prepro info file
    info_file.prepro.write(inputs)

    # Read list of parameters file, get nominal value, and create a dictionary
    params_dict = prepro.read_params(inputs["params_list_contents"],
                                     inputs["tracin_base_contents"])

    # Update the info file with information of list of parameters file
    paramfile.common.append_info(params_dict, inputs["info_file"])

    # Create a string template
    tracin_template = tracin.create_template(params_dict,
                                             inputs["tracin_base_contents"])

    # Create a directory structure based on the specified input
    prepro.create_dirtree(inputs, params_dict, tracin_template)


def cli_execute():
    """trace-simexp execution step command line interface"""

    from trace_simexp import execute
    from trace_simexp import info_file

    # Consolidate all the required inputs for post-processing phase
    exec_inputs = execute.get_input()

    # Otherwise, write the execute phase info file
    info_file.execute.write(exec_inputs)

    # Check if the directory structure structures already exists
    execute.check_dirtree(exec_inputs)

    # Commence the calculation in batches
    execute.run_batches(exec_inputs)


def cli_postpro():
    """trace-simexp post-processing step command line interface"""

    from trace_simexp import postpro
    from trace_simexp import info_file

    # Consolidate all the required inputs for post-processing phase
    postpro_inputs = postpro.get_input()

    # Write the execute phase info file
    info_file.postpro.write(postpro_inputs)

    # Commence the conversion
    postpro.dmx2csv(postpro_inputs)


def cli_reset():
    """trace-simexp reset command line interface"""
    from trace_simexp import reset, prepro, execute, postpro

    # Get all inputs
    reset_inputs = reset.get_input()

    # Reset phase
    if reset_inputs["phase"] == "prepro":
        prepro.reset(reset_inputs)
    elif reset_inputs["phase"] == "exec":
        execute.reset(reset_inputs)
    elif reset_inputs["phase"] == "postpro":
        postpro.reset(reset_inputs)
