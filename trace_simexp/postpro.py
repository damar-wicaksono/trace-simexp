"""Main module for post-processing activities - Post-processing Phase
"""

__author__ = "Damar Wicaksono"


def get_input():
    """Get all the inputs for post-processing phase of the simulation experiment

    The source of inputs are: command line arguments, exec.info file,
    prepro.info file, and list of trace variables

    :return: (dict) all the inputs for post-processing phase in a dictionary
    """
    from .task import aptscript
    from . import cmdln_args
    from . import info_file
    from . import util

    # Get command line arguments
    exec_info_fullname, exec_info_contents, \
    xtv_vars_fullname, xtv_vars_contents,\
    aptplot_exec, num_procs, postpro_filename = cmdln_args.postpro.get()

    # Read exec.info file
    prepro_info_fullname, samples = info_file.execute.read(exec_info_contents)

    # Read the prepro info file
    with open(prepro_info_fullname, "rt") as prepro_info:
        prepro_info_contents = prepro_info.read().splitlines()

    # Read prepro.info file
    base_dir, case_name, params_list_name, dm_name, avail_samples = \
        info_file.prepro.read(prepro_info_contents)

    # Read the list of TRACE variables name
    xtv_vars = aptscript.read(xtv_vars_contents)

    # Extract the name of the list of xtv variables file
    xtv_vars_name = xtv_vars_fullname.split("/")[-1].split(".")[0]

    # Get the host name
    hostname = util.get_hostname()

    # Combine all parameters in a python dictionary
    postpro_inputs = {"exec_info_fullname": exec_info_fullname,
                      "exec_info_contents": exec_info_contents,
                      "xtv_vars_fullname": xtv_vars_fullname,
                      "xtv_vars_name": xtv_vars_name,
                      "xtv_vars": xtv_vars,
                      "aptplot_exec": aptplot_exec,
                      "num_procs": num_procs,
                      "samples": samples,
                      "prepro_info_fullname": prepro_info_fullname,
                      "base_dir": base_dir,
                      "case_name": case_name,
                      "params_list_name": params_list_name,
                      "dm_name": dm_name,
                      "hostname": hostname
                      }

    # Write to a file the summary of execution phase parameters
    if postpro_filename is None:
        postpro_filename = info_file.common.make_filename(postpro_inputs, 
                                                          "postpro")

    info_file.postpro.write(postpro_inputs, postpro_filename)
    postpro_inputs["info_file"] = postpro_filename

    return postpro_inputs


def dmx2csv(postpro_inputs: dict):
    """Driver function to convert the dmx or xtv file into a csv file

    :param postpro_inputs: (dict) the input parameters for post-processing phase
    """
    from .util import link_exec
    from .util import create_iter
    from .util import make_dirnames
    from .util import make_auxfilenames
    from .task import dmx2csv

    # Check if the aptplot_exec is in the path
    if len(postpro_inputs["aptplot_exec"].split("/")) > 1:
        aptplot_is_in_path = False
        aptplot_exec_name = postpro_inputs["aptplot_exec"].split("/")[-1]
    else:
        aptplot_is_in_path = True

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
            aptplot_exec = "./{}" .format(aptplot_exec_name)

        # Execute the dmx commands
        dmx2csv.run(aptplot_exec,
                    postpro_inputs["xtv_vars"],
                    postpro_inputs["xtv_vars_name"],
                    run_names, run_dirnames, 
                    postpro_inputs["info_file"])


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
        csv_fullname = "{}/{}" .format(run_dirname, csv_filename)
        csv_fullnames.append(csv_fullname)

    # Do the cleanup
    if query_yes_no("Delete all CSV files?", default="no"):

        # Append the info file
        with open(postpro_inputs["info_file"], "a") as info_file:
            info_file.writelines("***Removing csv files***\n")
            for csv_file in csv_fullnames:
                if os.path.isfile(csv_file):
                    info_file.writelines("Removing: {}\n" .format(csv_file))
                else:
                    info_file.writelines("File not found: {}\n" 
                                         .format(csv_file))

        # Delete
        clean.rm_files(csv_fullnames)

