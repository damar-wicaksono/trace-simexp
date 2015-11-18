""" Module to create batches of TRACE runs and execute them
"""

import itertools

__author__ = "Damar Wicaksono"


def run(exec_inputs: dict):
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

    num_samples = len(exec_inputs["samples"])
    case_name = exec_inputs["case_name"]
    for batch_iter in create_iter(num_samples, exec_inputs["num_procs"]):

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
        trace.run(trace_commands, log_fullnames, run_dirnames)
        
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
        xtv2dmx.run(xtv2dmx_commands, log_fullnames, run_dirnames)

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
            clean.run(aux_files)


def make_dirnames(list_iter: list,
                  exec_inputs: dict,
                  scratch_flag: bool=False) -> list:
    """Make a complete run directory fullname

    :param list_iter: (list) the iterator converted to a list of integer
    :param exec_inputs: (dict) the execution phase inputs in dictionary
    :param scratch_flag: (bool) boolean flag to indicate whether the base dir is
        in the run directory or scratch directory. The downstream naming will be
        identical.
    :return: list of string with complete directory fullname
    """
    run_dirnames = []

    if scratch_flag:
        base_dir = exec_inputs["scratch_dir"]
    else:
        base_dir = exec_inputs["base_dir"]

    for i in list_iter:
        run_dirname = "{}/{}/{}-{}/{}-run_{}" .format(
            base_dir,
            exec_inputs["case_name"],
            exec_inputs["params_list_name"],
            exec_inputs["dm_name"],
            exec_inputs["case_name"],
            i
        )
        run_dirnames.append(run_dirname)

    return run_dirnames


def make_auxfilenames(list_iter: list, case_name: str, aux_ext: str) -> list:
    """Create a TRACE files with customized extension (used as auxiliary files)

    :param list_iter: (list) the iterator converted to a list of integer
    :param case_name: (str) the case name
    :param aux_ext: (str) the extension of auxiliary file
    :return: list of string with auxiliary filenames according to the iterator
    """
    aux_filenames = []

    for i in list_iter:
        aux_filename = "{}-run_{}{}" .format(case_name, i, aux_ext)
        aux_filenames.append(aux_filename)

    return aux_filenames


def create_iter(num_samples: int, num_processors: int) -> itertools.islice:
    """Create a list of iterator in batch size.

    The batch size is depending on the number of processors.
    Batch runs are required to maximize processor occupancy

    **References:**
    Taken from
    http://code.activestate.com/recipes/303279-getting-items-in-batches/

    :param num_samples: (int) number of samples to be run
    :param num_processors: (int) number of available processors, the size
        of batch
    :returns: (iterator) an iterator in batch size
    """
    import itertools

    iterable = range(0, num_samples)
    source_iter = iter(iterable)
    while True:
        batch_iter = itertools.islice(source_iter, num_processors)
        yield itertools.chain([next(batch_iter)], batch_iter)
