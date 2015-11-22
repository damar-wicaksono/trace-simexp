"""Main module for execute functionalities - Execute Phase
"""

__author__ = "Damar Wicaksono"


def get_input(info_filename: str=None) -> dict:
    """Get the command line arguments, read the info file, and construct dict()

    The source of inputs are: command line arguments and prepro.info file

    :return: (dict) the inputs collected as dictionary
    """
    from . import cmdln_args
    from . import info_file
    from . import util

    inputs = dict()

    # Read the command line arguments
    samples, prepro_infofile, num_procs, scratch_dir, trace_exec, \
        xtv2dmx_exec = cmdln_args.execute.get()

    # Read the pre-processing phase info file
    base_dir, case_name, params_list_name, dm_name, avail_samples = \
        info_file.prepro.read(prepro_infofile)

    # Check if samples is within the available samples
    if isinstance(samples, bool) and samples:
        samples = avail_samples
    elif set(samples) < set(avail_samples):
        samples = samples
    else:
        raise ValueError("Requested samples is not part of the available ones")

    # Get the name of the machine (hostname)
    hostname = util.get_hostname()

    # Construct the dictionary
    exec_inputs = {
        "prepro_info": prepro_infofile,
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

    # todo: Check the validity of the inputs

    # Write to a file the summary of execution phase parameters
    if info_filename is not None:
        info_file.execute.write(exec_inputs, info_filename)
        exec_inputs["exec_info"] = info_filename
    else:
        info_filename = info_file.common.make_filename(exec_inputs, "exec")
        info_file.execute.write(exec_inputs, info_filename)
        exec_inputs["exec_info"] = info_filename

    return exec_inputs


def run_batches(exec_inputs: dict):
    """Driver function to prepare run directory and execute trace in batches

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
    from .util import create_iter
    from .util import make_dirnames
    from .util import make_auxfilenames

    num_samples = len(exec_inputs["samples"])
    case_name = exec_inputs["case_name"]
    batch_int = 1
    for batch_iter in create_iter(num_samples, exec_inputs["num_procs"]):

        # Append the exec.info
        info_file = open(exec_inputs["exec_info"], "a")
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

        # Create bunch of scratch directory names
        scratch_dirnames = make_dirnames(list_iter, exec_inputs, True)

        # Create bunch of xtv files
        xtv_filenames = make_auxfilenames(list_iter, case_name, ".xtv")
        xtv_fullnames = ["{}/{}" .format(a, b) for a, b in zip(run_dirnames,
                                                               xtv_filenames)]
        scratch_xtv_fullnames = [
            "{}/{}" .format(a, b) for a, b in zip(scratch_dirnames,
                                                  xtv_filenames)]

        # Create bunch of trace commands
        inp_filenames = make_auxfilenames(list_iter, case_name, "")
        trace_commands = trace.make_commands(exec_inputs, inp_filenames)

        # Link the xtv in the scratch
        trace.link_xtv(scratch_dirnames, xtv_fullnames, scratch_xtv_fullnames)

        # Execute TRACE commands
        trace.run(trace_commands, log_fullnames,
                  run_dirnames, exec_inputs["exec_info"])

        # Create bunch of dmx files
        dmx_filenames = make_auxfilenames(list_iter, case_name, ".dmx")
        dmx_fullnames = ["{}/{}" .format(a, b) for a, b in zip(run_dirnames,
                                                               dmx_filenames)]
        scratch_dmx_fullnames = [
            "{}/{}" .format(a, b) for a, b in zip(scratch_dirnames,
                                                  dmx_filenames)]

        # Link the dmx in the scratch to the one in run directory
        xtv2dmx.link_dmx(dmx_fullnames, scratch_dmx_fullnames)

        # Create bunch of xtv2dmx commands
        xtv2dmx_commands = xtv2dmx.make_commands(exec_inputs,
                                                 xtv_filenames,
                                                 dmx_filenames)

        # Execute xtv2dmx commands
        xtv2dmx.run(xtv2dmx_commands, log_fullnames,
                    run_dirnames, exec_inputs["exec_info"])

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
        aux_files_list.append(scratch_xtv_fullnames)

        # Clean up TRACE directories
        for aux_files in aux_files_list:
            clean.rm_files(aux_files)
