""" Module to create batches of TRACE runs and execute them
"""

import itertools

__author__ = "Damar Wicaksono"


def run(exec_inputs: dict):
    """

    :param exec_inputs:
    :return:
    """
    num_samples = len(exec_inputs["samples"])
    for batch_iter in create_iter(num_samples, exec_inputs["num_procs"]):
        create(batch_iter, exec_inputs)

        # Create bunch of run directory names
        run_dirname = "{}/{}/{}-{}/{}-{}" .format(
            exec_inputs["base_dir"],
            exec_inputs["case_name"],
            exec_inputs["params_list_name"],
            exec_inputs["dm_name"],
            exec_inputs["case_name"],
            i
        )
        # Create bunch of log files
        # Create bunch of scratch directory names
        # Create bunch of trace commands
        # Execute TRACE commands
        # Create bunch of xtv2dmx commands
        # Execute xtv2dmx commands
        # Create bunch of .dif files
        # Create bunch of .tpr files
        # Create bunch of .out files
        # Create bunch of .ech files
        # Create bunch of .msg files
        # Clean up TRACE directories


def create(batch_iterator: itertools.islice, exec_inputs: dict):
    r"""Create an iterator of total runs in batch size

    :param num_samples: (int) number of samples to run
    :param num_processors: (int) number of available processors / batch size
    :return: (iterator) an iterator
    """
    log_files = []
    run_dirnames = []
    scratch_dirnames = []
    trace_cmds = []
    xtv2dmx_cmds = []

    # Iterate the passed iterator
    for i in batch_iterator:

        # Create a list of files
        run_dirname = "{}/{}/{}-{}/{}-run"
        run_scratch_dir = ""
        run_filename = ""
        run_dif = ""
        run_ech = ""
    # Create List of

        # Bunch of log files
        log_filename = ""
        log_fullname = ""
        log_files.append(log_fullname)

    # Bunch of working directories
    # Bunch of scratch directories
    # Bunch of TRACE execution commands
    # Bunch of XTV conversion commands
    # Bunch of the number of sample
    # Bunch of XTV in the scratch
    # Bunch of TRACE .dif files
    # Bunch of TRACE .tpr files
    # Bunch of TRACE .out files
    # Bunch of TRACE .ech files
    # Bunch of TRACE .msg files


def exec_trace(log_files: list, run_dirnames: list,
               scratch_dirnames: list, trace_cmds: list,
               xtv2dmx_cmds: list):
    r"""Execute multiple TRACE input deck

    :return:
    """
    import subprocess


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