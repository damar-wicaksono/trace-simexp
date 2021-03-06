# -*- coding: utf-8 -*-
"""
    trace_simexp.postpro
    ********************
    
    Main module for the post-processing related activities
"""

__author__ = "Damar Wicaksono"


def get_input():
    """Get all the inputs for post-processing phase of the experiment runs

    The source of inputs are: command line arguments, exec.info file, 
    and list of trace graphic variables

    :return: all the inputs for post-processing phase in a dictionary
    
    +----------------------+--------------------------------------------------+
    | Key                  | Value                                            |
    +======================+==================================================+
    | prepro_info_name     | (str) The name of the passed prepro infofile     |
    +----------------------+--------------------------------------------------+
    | prepro_info_fullname | (str) The name and full path of the passed prepro|
    |                      | infofile                                         |
    +----------------------+--------------------------------------------------+
    | exec_info_name       | (str) The name of the passed execute infofile    |
    +----------------------+--------------------------------------------------+
    | exec_info_fullname   | (str) The name and full path of the passed       |
    |                      | execute infofile                                 |
    +----------------------+--------------------------------------------------+
    | exec_info_contents   | (list, str) The contents of the execute infofile |
    +----------------------+--------------------------------------------------+
    | xtv_vars_name        | (str or None) The name of the list of TRACE      |
    |                      | graphics variable file                           |
    +----------------------+--------------------------------------------------+
    | xtv_vars_fullname    | (str) The name and full path of the list of TRACE|
    |                      | graphics variable file                           |
    +----------------------+--------------------------------------------------+
    | xtv_vars             | (list, str) The list of TRACE graphic variables, |
    |                      | parsed from the specified file                   |
    +----------------------+--------------------------------------------------+
    | aptplot_exec         | (str) The executable for APTPLOT tool either the |
    |                      | full path or assumed to be accessible in the path|
    +----------------------+--------------------------------------------------+
    | num_procs            | (int) The number of processors to post-process   |
    |                      | TRACE perturbed cases outputs simultaneously     |
    +----------------------+--------------------------------------------------+
    | samples              | (list, int) List of samples to be executed       |
    |                      | must be in accordance between prepro and command |
    |                      | line arguments                                   |
    +----------------------+--------------------------------------------------+
    | base_dir             | (str) The base directory of the simulation       |
    |                      | campaign                                         |
    +----------------------+--------------------------------------------------+
    | case_name            | (str) The name of the base TRACE input deck      |
    +----------------------+--------------------------------------------------+
    | params_list_name     | (str) The name of the list of parameters file    |
    +----------------------+--------------------------------------------------+
    | dm_name              | (str) The name of the design matrix file         |
    +----------------------+--------------------------------------------------+
    | hostname             | (str) The name of the machine the campaign was   |
    |                      | executed                                         |
    +----------------------+--------------------------------------------------+
    | overwrite            | (bool) The flag to continue the pre-processing   |
    |                      | step even though info files and directory        |
    |                      | structures already exist                         |
    +----------------------+--------------------------------------------------+
    | info_file            | (str) The filename of the post-pro infofile      |
    +----------------------+--------------------------------------------------+
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
        samples, overwrite, postpro_filename = cmdln_args.postpro.get()

    # Parse exec.info file
    prepro_info_fullname, base_dir, case_name, params_list_name, \
        dm_name, scratch_dir, \
        avail_samples = execute.read(exec_info_contents)

    # Extract the name of the exec.info file
    exec_info_name = util.get_name(exec_info_fullname, incl_ext=True)

    # Extract the name of the list of xtv variables file
    xtv_vars_name = util.get_name(xtv_vars_fullname, incl_ext=False)

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
                      "hostname": hostname,
                      "overwrite": overwrite,
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


def check_dirtree(postpro_inputs: dict):
    """Check the run directory structure whether it is clean for post-processing

    "Clean" means there is at the very least the appropriate dmx file and no 
    overlapping csv file. If there is no dmx then raise error, if there is 
    overlapping csv, check if overwrite is allowed

    :param postpro_inputs: the postpro phase inputs
    :return: list of dirty directory tree
    """
    import os
    from .util import make_dirnames
    from .util import make_auxfilenames
    from .task import clean

    dirty_dirs = []
    dirty_dir_nums = []
    empty_dirs = []

    # Create the list of run directories
    run_dirnames = make_dirnames(postpro_inputs["samples"], postpro_inputs, False)
    # Create the list of TRACE dmx files not to be removed
    dmx_filenames = make_auxfilenames(postpro_inputs["samples"],
                                      postpro_inputs["case_name"],
                                      ".dmx")
    # Create the list of CSV files
    csv_filenames =  make_auxfilenames(postpro_inputs["samples"],
                                       postpro_inputs["case_name"],
                                       "-{}.csv" .format(
                                           postpro_inputs["xtv_vars_name"]))
    # CSV fullnames
    csv_fullnames = [os.path.join(a, b) for a, b in zip(run_dirnames,
                                                        csv_filenames)]

    # Loop over run directories and input filenames and grab the invalid ones
    for i, (run_dirname, dmx_filename, csv_filename) in \
            enumerate(zip(run_dirnames, dmx_filenames, csv_filenames)):
        if csv_filename in os.listdir(run_dirname):
            dirty_dirs.append(run_dirname)
            dirty_dir_nums.append(postpro_inputs["samples"][i])
        if dmx_filename not in os.listdir(run_dirname):
            empty_dirs.append(run_dirname)

    # Check if there is empty run directory
    if empty_dirs:
        for empty_dir in empty_dirs:
            print("{} does not contain the correct input file!"
                  .format(empty_dir))
        raise ValueError("Some input file does not exist!")
    # Check if there is dirty run directory
    elif dirty_dirs:
        if not postpro_inputs["overwrite"]:
            for dirty_dir in dirty_dirs:
                print("{} run directory is dirty!"
                      .format(dirty_dir))
            raise ValueError("One or more run directories are dirty and no"
                             " overwrite flag!")
        else:
            # Clean the directory first
            clean.rm_files(csv_fullnames)
    else:
        pass


def reset(postpro_inputs: dict):
    """Reset the directory structures to the execute phase state

    :param postpro_inputs: the input parameters for post-processing phase
    """
    import os
    from .util import make_dirnames
    from .util import make_auxfilenames
    from .util import query_yes_no
    from .task import clean

    dirty_nums = 0

    # Create the list of run directories
    run_dirnames = make_dirnames(postpro_inputs["samples"], postpro_inputs,
                                 False)

    # Create the list of CSV files
    csv_filenames = make_auxfilenames(postpro_inputs["samples"],
                                      postpro_inputs["case_name"],
                                      "-{}.csv".format(
                                          postpro_inputs["xtv_vars_name"]))
    # CSV fullnames
    csv_fullnames = [os.path.join(a, b) for a, b in zip(run_dirnames,
                                                        csv_filenames)]

    # Print message
    for csv_fullname in csv_fullnames:
        if os.path.isfile(csv_fullname):
            print("{} will be deleted." .format(csv_fullname))
            dirty_nums += 1

    # Do the cleanup
    if dirty_nums > 0:
        if query_yes_no("Delete all CSV files?", default="no"):
            clean.rm_files(csv_fullnames)
    else:
        print("No csv file can be found. Aborting...")

