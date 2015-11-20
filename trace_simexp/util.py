"""Module with utility functions to support the whole trace_simexp package
"""

import itertools


__author__ = "Damar Wicaksono"


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


def get_hostname() -> str:
    """Get the hostname from the command line utility `hostname`

    :return: (str) of the hostname
    """
    import subprocess

    p = subprocess.Popen(["hostname"], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    return p.communicate()[0].rstrip().decode("utf-8")
