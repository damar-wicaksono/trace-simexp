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


def create(batch_iterator: itertools.islice, exec_inputs: dict):
    r"""Create an iterator of total runs in batch size

    :param num_samples: (int) number of samples to run
    :param num_processors: (int) number of available processors / batch size
    :return: (iterator) an iterator
    """
    # Iterate the passed iterator
    for i in batch_iterator:
        print(i)
    # Create List of
    # Bunch of log files
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



def exec_trace():
    """Execute multiple

    :return:
    """
    return None


def clean_trace():
    """Clean TRACE Directories

    :return:
    """
    return None


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