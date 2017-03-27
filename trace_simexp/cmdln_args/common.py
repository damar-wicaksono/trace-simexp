# -*- coding: utf-8 -*-
"""
    trace_simexp.cmdln_args.common
    ******************************

    Some common functions to support parsing the command line arguments for
    each phase
"""
import os

__author__ = "Damar Wicaksono"


def check_samples_argument(num_samples: list = None,
                           num_range: list = None,
                           all_samples: bool = False):
    """Check the validity of specified samples argument

        Note that the check is only for the validity of argument, not its
        consistency with the available samples

    :param num_samples: the list of select samples
    :param num_range: the range of samples, between two numbers, inclusive
    :param all_samples: Flag to pre-process/execute/post-process all samples
    """
    import argparse

    parser = argparse.ArgumentParser()

    if num_samples is not None and num_range is not None \
            and all_samples:
        parser.error("Ambiguous, -ns, -nr, and -as cannot all be present!")
    elif num_samples is not None and num_range is not None:
        parser.error("Ambiguous, -ns or -nr cannot both be present!")
    elif num_samples is not None and all_samples:
        parser.error("Ambiguous, -ns or -as cannot both be present!")
    elif num_range is not None and all_samples:
        parser.error("Ambiguous, -nr or -as cannot both be present!")
    else:
        pass


def get_samples(select_samples: list, avail_samples: list) -> list:
    """Get while checking the validity of the requested samples

    :param select_samples: The selected samples
    :param avail_samples: The list of all available samples based on the range
    :return: The selected samples, verified
    """

    # Sample number has to be positive
    if True in [_ < 0 for _ in select_samples]:
        raise ValueError(
            "Number of samples with -ns has to be strictly positive!")
    # Sample number has to be within the available sample
    elif False in [_ in avail_samples for _ in select_samples]:
        raise ValueError(
            "Some or all selected samples are not available in the design")

    return select_samples


def expand_path(file_or_dirname: str, if_none: str = os.getcwd()) -> str:
    """Expand filename or directory name to an absolute path

    :param file_or_dirname: The filename or directory name, either relative or
        absolute
    :param if_none: What to do if None is passed as file_or_dirname
    :return: The full path of file or directory if given, or if_none
    """
    if file_or_dirname:
        return os.path.abspath(file_or_dirname)
    else:
        return if_none


def get_fullname_and_contents(file_object, dsv: bool = False) -> tuple:
    """Expand filename to an absolute path and get the contents of it

    :param file_object: The file object read by argparse
    :param dsv: Flag whether the file is Delimiter Separated Value
    :return: A tuple with following contents
        (str) the filename in full (path + filename)
        (list) the contents of the file as list
    """
    from .. import util

    fullname = os.path.abspath(file_object.name)

    with file_object as file:
        if dsv:
            file_contents = util.parse_csv(file)
        else:
            file_contents = file.read().splitlines()

    return fullname, file_contents


def get_executable(exec_name: str) -> str:
    """Check and get the executable, whether in PATH or somewhere else
    
    :param exec_name: the name of the executable
    :return: the name of the executable, verified. If it is not on the path,
        the filename + path will be returned
    """
    from .. import util

    if util.cmd_exists(exec_name):
        # Assume the executable is in the path
        return exec_name
    elif util.exe_exists(exec_name):
        # Maybe it is specified with directory instead, then return full path
        return os.path.abspath(exec_name)
    else:
        # Not found, raise error
        raise ValueError("The executable {} not found!" .format(exec_name))
