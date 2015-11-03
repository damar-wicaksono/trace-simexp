""" Module to create batches of TRACE runs and execute them
"""

import itertools

__author__ = "Damar Wicaksono"


def run(exec_inputs: dict):
    """

    :param exec_inputs:
    :return:
    """
    from .batch_process import trace

    num_samples = len(exec_inputs["samples"])
    for batch_iter in create_iter(num_samples, exec_inputs["num_procs"]):

        # Repeat the iterator multiple times according to the number of calls
        batch_iter_rep = itertools.tee(batch_iter, 9)

        # Create bunch of run directory names
        run_dirnames = make_dirnames(batch_iter_rep[0], exec_inputs, False)

        # Create bunch of log files
        log_filenames = make_auxfilenames(batch_iter_rep[1], exec_inputs, "log")
        log_fullnames = ["{}/{}" .format(a, b) for a, b in zip(run_dirnames,
                                                               log_filenames)]

        # Create bunch of scratch directory names
        scratch_dirnames = make_dirnames(batch_iter_rep[2], exec_inputs, True)

        # Create bunch of trace commands
        trace_commands = make_trccommands(batch_iter_rep[3], exec_inputs)

        # Execute TRACE commands
        trace.run(run_dirnames, scratch_dirnames, trace_commands, log_fullnames)

        # Create bunch of xtv2dmx commands

        # Execute xtv2dmx commands

        # Start to clean up things
        # Create bunch of .dif files
        dif_filenames = make_auxfilenames(batch_iter_rep[4], exec_inputs, "dif")
        dif_fullnames = ["{}/{}" .format(a, b) for a, b in zip(run_dirnames,
                                                               dif_filenames)]

        # Create bunch of .tpr files
        tpr_filenames = make_auxfilenames(batch_iter_rep[5], exec_inputs, "tpr")
        tpr_fullnames = ["{}/{}" .format(a, b) for a, b in zip(run_dirnames,
                                                               tpr_filenames)]

        # Create bunch of .out files
        out_filenames = make_auxfilenames(batch_iter_rep[6], exec_inputs, "out")
        out_fullnames = ["{}/{}" .format(a, b) for a, b in zip(run_dirnames,
                                                               out_filenames)]

        # Create bunch of .ech files
        ech_filenames = make_auxfilenames(batch_iter_rep[7], exec_inputs, "ech")
        ech_fullnames = ["{}/{}" .format(a, b) for a, b in zip(run_dirnames,
                                                               ech_filenames)]

        # Create bunch of .msg files
        msg_filenames = make_auxfilenames(batch_iter_rep[8], exec_inputs, "msg")
        msg_fullnames = ["{}/{}" .format(a, b) for a, b in zip(run_dirnames,
                                                               msg_filenames)]

        # Clean up TRACE directories


def make_dirnames(batch_iterator: itertools.islice,
                  exec_inputs: dict,
                  scratch_flag: bool=False) -> list:
    """

    :param batch_iterator:
    :param exec_inputs:
    :return:
    """
    run_dirnames = []

    if scratch_flag:
        base_dir = exec_inputs["scratch_dir"]
    else:
        base_dir = exec_inputs["base_dir"]

    for i in batch_iterator:
        run_dirname = "{}/{}/{}-{}/{}-{}" .format(
            base_dir,
            exec_inputs["case_name"],
            exec_inputs["params_list_name"],
            exec_inputs["dm_name"],
            exec_inputs["case_name"],
            i+1
        )
        run_dirnames.append(run_dirname)

    return run_dirnames


def make_auxfilenames(batch_iterator: itertools.islice,
                      exec_inputs: dict,
                      aux_ext: str) -> list:
    """

    :param batch_iterator:
    :param exec_inputs:
    :param aux_ext: the extension of auxiliary file
    :return:
    """
    aux_filenames = []

    for i in batch_iterator:
        aux_filename = "{}-run_{}.{}" .format(exec_inputs["case_name"],
                                              i+1,
                                              aux_ext)
        aux_filenames.append(aux_filename)


    return aux_filenames


def make_trccommands(batch_iterator: itertools.islice,
                     exec_inputs: dict) -> list:
    """

    :param batch_iterator:
    :param exec_inputs:
    :return:
    """
    trace_commands = []

    for i in batch_iterator:
        inp_filename = "{}-run_{}" .format(exec_inputs["case_name"], i+1)
        trace_command = [exec_inputs["trace_exec"], "-p", inp_filename]
        trace_commands.append(trace_command)

    return trace_commands


def exec_xtv2dmx(scratch_dirnames: list, xtv2dmx_cmds: list):
    r"""Convert xtv files to dmx file to save some space

    :param scratch_dirnames:
    :param xtv2dmx_cmds:
    :return:
    """
    return None


def clean_trace(scratch_xtvs: list, link_xtvs: list,
                tpr_files: list, dif_files: list,
                ech_files: list, msg_file: list,
                out_files: list):
    """Clean TRACE Directories

    :return:
    """
    import subprocess


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