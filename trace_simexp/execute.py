"""Main module for execute functionalities - Execute Phase
"""

__author__ = "Damar Wicaksono"


def get_input() -> dict:
    """Get the command line arguments, read the info file, and construct dict()

    The source of inputs are: command line arguments and prepro.info file

    :return: (dict) the inputs collected as dictionary
    """
    from . import cmdln_args
    from . import info_file
    from . import util

    # Read the command line arguments
    samples, \
        prepro_info_fullname, prepro_info_contents, \
        num_procs, scratch_dir, \
        trace_exec, xtv2dmx_exec, exec_filename = cmdln_args.execute.get()

    # Read the pre-processing phase info file
    base_dir, case_name, params_list_name, dm_name, avail_samples = \
        info_file.prepro.read(prepro_info_contents)

    # Check if samples is within the available samples
    if isinstance(samples, bool) and samples:
        samples = avail_samples
    elif set(samples) <= set(avail_samples):
        samples = samples
    else:
        raise ValueError("Requested samples is not part of the available ones")

    # Get the name of the prepro info file
    prepro_info_name = prepro_info_fullname.split("/")[-1]

    # Get the name of the machine (hostname)
    hostname = util.get_hostname()

    # Construct the dictionary
    exec_inputs = {
        "prepro_info_name": prepro_info_name,
        "prepro_info_contents": prepro_info_contents,
        "num_procs": num_procs,
        "scratch_dir": scratch_dir,
        "trace_exec": trace_exec,
        "xtv2dmx_exec": xtv2dmx_exec,
        "base_dir": base_dir,
        "case_name": case_name,
        "params_list_name": params_list_name,
        "dm_name": dm_name,
        "samples": samples,
        "hostname": hostname
    }

    # Write to a file the summary of execution phase parameters
    if exec_filename is None:
        exec_filename = info_file.common.make_filename(exec_inputs, "exec")

    info_file.execute.write(exec_inputs, exec_filename)
    exec_inputs["info_file"] = exec_filename

    return exec_inputs


def run_batches(exec_inputs: dict):
    """Driver function to prepare run directory and execute TRACE in batches

    1. The directories are prepared by making a link between dummy xtv in the
       run directory and its corresponding scratch directory.
    2. All the trace jobs are executed in parallel depending on the available
       number of CPUs
    3. After execution, a link is made between a dummy dmx file in the run
       directory and its corresponding scratch directory.
    4. Convert the xtv into dmx
    5. Do directory clean up after TRACE execution and XTV conversion, all
       unnecessary auxiliary files are removed to save disk space. The original
       xtv file and its link are also removed.

    :param exec_inputs: (dict) the inputs for execution phase
    """
    from .task import trace
    from .task import xtv2dmx
    from .task import clean
    from .util import link_exec
    from .util import create_iter
    from .util import make_dirnames
    from .util import make_auxfilenames

    # Check if the trace_executable and xtv2dmx_executable are in the path
    if len(exec_inputs["trace_exec"].split("/")) > 1:
        trace_is_in_path = False
        trace_exec_name = exec_inputs["trace_exec"].split("/")[-1]
    else:
        trace_is_in_path = True
    if len(exec_inputs["xtv2dmx_exec"].split("/")) > 1:
        xtv2dmx_is_in_path = False
        xtv2dmx_exec_name = exec_inputs["xtv2dmx_exec"].split("/")[-1]
    else:
        xtv2dmx_is_in_path = True

    num_samples = len(exec_inputs["samples"])
    case_name = exec_inputs["case_name"]
    batch_int = 1
    for batch_iter in create_iter(num_samples, exec_inputs["num_procs"]):

        # Append the exec.info
        info_file = open(exec_inputs["info_file"], "a")
        info_file.writelines("*** Batch Execution - {:5d} ***\n"
                             .format(batch_int))
        info_file.close()
        batch_int += 1

        # Put the iterator from create_iter into a list for re-usage
        # Use the samples instead of the bare iterator
        list_iter = [exec_inputs["samples"][i] for i in list(batch_iter)]

        # Create bunch of run directory names
        run_dirnames = make_dirnames(list_iter, exec_inputs, False)

        # Create bunch of log files
        log_filenames = make_auxfilenames(list_iter, case_name, ".log")
        log_fullnames = ["{}/{}" .format(a, b) for a, b in zip(run_dirnames,
                                                               log_filenames)]

        # Create bunch of xtv files
        xtv_filenames = make_auxfilenames(list_iter, case_name, ".xtv")
        xtv_fullnames = ["{}/{}" .format(a, b) for a, b in zip(run_dirnames,
                                                               xtv_filenames)]

        if exec_inputs["scratch_dir"] is not None:
            # If scratch directory specified make the symbolic links
            # Create bunch of scratch directory names
            scratch_dirnames = make_dirnames(list_iter, exec_inputs, True)
            scratch_xtv_fullnames = [
                "{}/{}".format(a, b) for a, b in zip(scratch_dirnames,
                                                     xtv_filenames)]
            # Link the xtv in the scratch
            trace.link_xtv(scratch_dirnames, xtv_fullnames,
                           scratch_xtv_fullnames)

        # Create a bunch of trace input deck to be passed to the exec (no ext)
        inp_filenames = make_auxfilenames(list_iter, case_name, "")

        # If TRACE executable not in the path, create a symbolic link in run dir
        if trace_is_in_path:
            trace_exec = exec_inputs["trace_exec"]
        else:
            for run_dirname in run_dirnames:
                link_exec(exec_inputs["trace_exec"], run_dirname)
            trace_exec = "./{}" .format(trace_exec_name)

        # Create a bunch of trace commands
        trace_commands = trace.make_commands(trace_exec, inp_filenames)

        # Execute TRACE commands
        trace.run(trace_commands, log_fullnames,
                  run_dirnames, exec_inputs["info_file"])

        # Create bunch of dmx files
        dmx_filenames = make_auxfilenames(list_iter, case_name, ".dmx")
        dmx_fullnames = ["{}/{}" .format(a, b) for a, b in zip(run_dirnames,
                                                               dmx_filenames)]

        if exec_inputs["scratch_dir"] is not None:
            # If scratch directory specified make the symbolic links
            scratch_dmx_fullnames = [
                "{}/{}" .format(a, b) for a, b in zip(scratch_dirnames,
                                                      dmx_filenames)]

            # Link the dmx in the scratch to the one in run directory
            xtv2dmx.link_dmx(dmx_fullnames, scratch_dmx_fullnames)

        # If XTV2DMX exec. not in the path, create a symbolic link in run dir
        if xtv2dmx_is_in_path:
            xtv2dmx_exec = exec_inputs["trace_exec"]
        else:
            for run_dirname in run_dirnames:
                link_exec(exec_inputs["xtv2dmx_exec"], run_dirname)
            xtv2dmx_exec = "./{}" .format(xtv2dmx_exec_name)

        # Create bunch of xtv2dmx commands
        xtv2dmx_commands = xtv2dmx.make_commands(xtv2dmx_exec,
                                                 xtv_filenames,
                                                 dmx_filenames)

        # Execute xtv2dmx commands
        xtv2dmx.run(xtv2dmx_commands, log_fullnames,
                    run_dirnames, exec_inputs["info_file"])

        # Start to clean up things
        aux_files_list = []

        # Create bunch of .dif files
        dif_filenames = make_auxfilenames(list_iter, case_name, ".dif")
        dif_fullnames = ["{}/{}" .format(a, b) for a, b in zip(run_dirnames,
                                                               dif_filenames)]
        aux_files_list.append(dif_fullnames)

        # Create bunch of .tpr files
        tpr_filenames = make_auxfilenames(list_iter, case_name, ".tpr")
        tpr_fullnames = ["{}/{}" .format(a, b) for a, b in zip(run_dirnames,
                                                               tpr_filenames)]
        aux_files_list.append(tpr_fullnames)

        # Create bunch of .out files
        out_filenames = make_auxfilenames(list_iter, case_name, ".out")
        out_fullnames = ["{}/{}" .format(a, b) for a, b in zip(run_dirnames,
                                                               out_filenames)]
        aux_files_list.append(out_fullnames)

        # Create bunch of .echo files
        ech_filenames = make_auxfilenames(list_iter, case_name, ".echo")
        ech_fullnames = ["{}/{}" .format(a, b) for a, b in zip(run_dirnames,
                                                               ech_filenames)]
        aux_files_list.append(ech_fullnames)

        # Create bunch of .msg files
        msg_filenames = make_auxfilenames(list_iter, case_name, ".msg")
        msg_fullnames = ["{}/{}" .format(a, b) for a, b in zip(run_dirnames,
                                                               msg_filenames)]
        aux_files_list.append(msg_fullnames)

        # Collect the xtv files
        aux_files_list.append(xtv_fullnames)
        if exec_inputs["scratch_dir"] is not None:
            aux_files_list.append(scratch_xtv_fullnames)

        # Collect all the symbolic link of executables (if exists)
        if not trace_is_in_path:
            trace_links = ["{}/{}" .format(run_dirname, trace_exec_name)
                           for run_dirname in run_dirnames]
            aux_files_list.append(trace_links)
        if not xtv2dmx_is_in_path:
            xtv2dmx_links = ["{}/{}" .format(run_dirname, xtv2dmx_exec_name)
                             for run_dirname in run_dirnames]
            aux_files_list.append(xtv2dmx_links)

        # Clean up TRACE directories
        for aux_files in aux_files_list:
            clean.rm_files(aux_files)


def reset(exec_inputs: dict):
    """Reset the directory structures to the pre-pro phase state

    :param exec_inputs: (dict) the input parameters for execute phase
    """
    import os
    from .util import query_yes_no
    from .util import make_dirnames
    from .util import make_auxfilenames
    from .task import clean

    # Create dmx link
    run_dirnames = make_dirnames(exec_inputs["samples"], exec_inputs, False)
    dmx_filenames = make_auxfilenames(exec_inputs["samples"],
                                      exec_inputs["case_name"],
                                      ".dmx")

    dmx_fullnames = ["{}/{}" .format(a, b) for a, b in zip(run_dirnames,
                                                           dmx_filenames)]

    # Create list of scratch directories
    scratch_dirnames = make_dirnames(exec_inputs["samples"], exec_inputs, True)

    # Create list of TRACE input files not to be removed
    inp_filenames = make_auxfilenames(exec_inputs["samples"],
                                      exec_inputs["case_name"],
                                      ".inp")

    if query_yes_no("Revert back to pre-pro state?", default="no"):

        # Append the info file
        with open(exec_inputs["info_file"], "a") as info_file:
            info_file.writelines("***Reverting back to Pre-pro***\n")
            for i, dmx_fullname in enumerate(dmx_fullnames):
                if os.path.islink(dmx_fullname):
                    info_file.writelines("Reverting: {}\n"
                                         .format(run_dirnames[i]))

        # Clean scratch dirs
        clean.rm_files(scratch_dirnames)

        # Clean dmx links
        clean.rm_files(dmx_fullnames)

        # Clean the rest
        clean.rm_except(run_dirnames, inp_filenames)

    else:
        pass
