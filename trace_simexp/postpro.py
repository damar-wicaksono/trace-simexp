# -*- coding: utf-8 -*-
"""
    trace_simexp.postpro
    ********************
    
    Main module for the post-processing related activities
"""

__author__ = "Damar Wicaksono"


def get_input():
    """Get all the inputs for post-processing phase of the simulation experiment

    The source of inputs are: command line arguments, exec.info file, 
    and list of trace graphic variables

    :return: all the inputs for post-processing phase in a dictionary
    """
    import os
    from .task import aptscript
    from . import cmdln_args
    from . import util
    from .info_file import common, execute
    from .cmdln_args.common import get_samples

    # Get command line arguments
    exec_info_fullname, exec_info_contents, \
        xtv_vars_fullname, xtv_vars_contents, \
        aptplot_exec, num_procs, \
        samples, postpro_filename = cmdln_args.postpro.get()

    # Parse exec.info file
    prepro_info_fullname, base_dir, case_name, params_list_name, \
        dm_name, scratch_dir, \
        avail_samples = execute.read(exec_info_contents)

    # Extract the name of the exec.info file
    exec_info_name = util.get_name(exec_info_fullname, incl_ext=True)

    # Extract the name of the list of xtv variables file
    xtv_vars_name = util.get_name(xtv_vars_fullname, incl_ext=True)

    # Extract the name of the prepro.info file
    prepro_info_name = util.get_name(prepro_info_fullname, incl_ext=True)

    # Sample has to be specified, otherwise all available in the pre-processing
    # info file will be processed. Check the way it was specified and get them
    # If it is boolean, then all available samples
    if isinstance(samples, bool) and samples:
        samples = avail_samples
    else:
        # Else check its validity with the available samples
        samples = get_samples(samples, avail_samples)

    # Check if the prepro.info from exec.info is the same as passed by user
    # if prepro_info_from_exec != prepro_info_name:
    #    raise ValueError("The passed repro.info name does not agree with the"
    #                     "one specified in the exec.info!\n"
    #                     "{:<16s}: {}\n"
    #                     "{:<16s}: {}" .format("-prepro argument",
    #                                           prepro_info_name,
    #                                           "exec.info",
    #                                           prepro_info_from_exec))

    # Parse prepro.info file
    # base_dir, case_name, params_list_name, dm_name, avail_samples = \
    #    info_file.prepro.read(prepro_info_contents)

    # Read the list of TRACE variables name
    xtv_vars = aptscript.read(xtv_vars_contents)

    # Get the host name
    hostname = util.get_hostname()

    # Combine all parameters in a python dictionary
    postpro_inputs = {"prepro_info_name": prepro_info_name,
                      "prepro_info_fullname": prepro_info_fullname,
                      "exec_info_name": exec_info_name,
                      "exec_info_fullname": exec_info_fullname,
                      "exec_info_contents": exec_info_contents,
                      "xtv_vars_name": xtv_vars_name,
                      "xtv_vars_fullname": xtv_vars_fullname,
                      "xtv_vars": xtv_vars,
                      "aptplot_exec": aptplot_exec,
                      "num_procs": num_procs,
                      "samples": samples,
                      "base_dir": base_dir,
                      "case_name": case_name,
                      "params_list_name": params_list_name,
                      "dm_name": dm_name,
                      "hostname": hostname
                      }

    # Create an infofile filename if not provided
    if os.path.isdir(postpro_filename):
        postpro_filename = os.path.join(postpro_filename,
                                        common.make_filename(postpro_inputs,
                                                             "postpro"))
    # Add new entry to the dictionary
    postpro_inputs["info_file"] = postpro_filename

    return postpro_inputs


def dmx2csv(postpro_inputs: dict):
    """Driver function to convert the dmx or xtv file into a csv file

    :param postpro_inputs: the input parameters for post-processing phase
    """
    from .task import dmx2csv
    from .task import clean
    from .util import link_exec
    from .util import create_iter
    from .util import make_dirnames
    from .util import make_auxfilenames
    from .util import exe_exists
    from .util import cmd_exists
    from .util import get_name

    # Check if the APTPLOT executable is in the path
    if cmd_exists(postpro_inputs["aptplot_exec"]):
        aptplot_is_in_path = True
    elif exe_exists(postpro_inputs["aptplot_exec"]):
        aptplot_is_in_path = False
        aptplot_exec_name = get_name(postpro_inputs["aptplot_exec"],
                                     incl_ext=True)

    num_samples = len(postpro_inputs["samples"])
    case_name = postpro_inputs["case_name"]
    batch_int = 1

    for batch_iter in create_iter(num_samples, postpro_inputs["num_procs"]):

        # Append the exec.info
        info_file = open(postpro_inputs["info_file"], "a")
        info_file.writelines("*** Batch Execution - {:5d} ***\n"
                             .format(batch_int))
        info_file.close()
        batch_int += 1

        # Put the iterator from create_iter into a list for re-usage
        # Use the samples instead of bare iterator
        list_iter = [postpro_inputs["samples"][i] for i in list(batch_iter)]

        # Create bunch of run directory names
        run_dirnames = make_dirnames(list_iter, postpro_inputs, False)

        # Create bunch of run names
        run_names = make_auxfilenames(list_iter, case_name, "")

        # If AptPlot executable not in path, create a symbolic link in run dir
        if aptplot_is_in_path:
            aptplot_exec = postpro_inputs["aptplot_exec"]
        else:
            for run_dirname in run_dirnames:
                link_exec(postpro_inputs["aptplot_exec"], run_dirname)
            aptplot_exec = "./{}".format(aptplot_exec_name)

        # Execute the dmx commands
        dmx2csv.run(aptplot_exec,
                    postpro_inputs["xtv_vars"],
                    postpro_inputs["xtv_vars_name"],
                    run_names, run_dirnames,
                    postpro_inputs["info_file"])

        # Clean up run directories from symbolic link
        if not aptplot_is_in_path:
            aptplot_links = ["{}/{}".format(run_dirname, aptplot_exec_name)
                             for run_dirname in run_dirnames]
            clean.rm_files(aptplot_links)


def reset(postpro_inputs: dict):
    """Reset the directory structures to the execute phase state

    :param postpro_inputs: (dict) the input parameters for post-processing phase
    """
    import os
    from .util import make_dirnames
    from .util import query_yes_no
    from .task import clean

    # Empty list
    csv_fullnames = list()

    # Create a list of csv files
    run_dirnames = make_dirnames(postpro_inputs["samples"],
                                 postpro_inputs,
                                 False)

    for i, run_dirname in enumerate(run_dirnames):
        csv_filename = "{}-run_{}-{}.csv" \
            .format(postpro_inputs["case_name"],
                    postpro_inputs["samples"][i],
                    postpro_inputs["xtv_vars_name"])
        csv_fullname = "{}/{}".format(run_dirname, csv_filename)
        csv_fullnames.append(csv_fullname)

    # Do the cleanup
    if query_yes_no("Delete all CSV files?", default="no"):

        # Append the info file
        with open(postpro_inputs["info_file"], "a") as info_file:
            info_file.writelines("***Removing csv files***\n")
            for csv_file in csv_fullnames:
                if os.path.isfile(csv_file):
                    info_file.writelines("Removing: {}\n".format(csv_file))
                else:
                    info_file.writelines("File not found: {}\n"
                                         .format(csv_file))

        # Delete
        clean.rm_files(csv_fullnames)
