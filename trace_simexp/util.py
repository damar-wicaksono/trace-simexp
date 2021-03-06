# -*- coding: utf-8 -*-
"""
    trace_simexp.util
    *****************

    Module with utility functions to support the whole trace_simexp package
"""
import itertools
import subprocess
import numpy as np

__author__ = "Damar Wicaksono"


def create_iter(num_samples: int, num_processors: int):
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
    iterable = range(0, num_samples)
    source_iter = iter(iterable)
    while True:
        batch_iter = itertools.islice(source_iter, num_processors)
        yield itertools.chain([next(batch_iter)], batch_iter)


def make_dirnames(list_iter: list,
                  dict_inputs: dict,
                  scratch_flag: bool=False) -> list:
    """Make a complete run directory fullname

    :param list_iter: the iterator converted to a list of integer
    :param dict_inputs: the inputs of a phase in dictionary
    :param scratch_flag: boolean flag to indicate whether the base dir is in
        the run directory or scratch directory. The downstream naming will be
        identical.
    :return: list of string with complete directory fullname
    """
    import os

    run_dirnames = []

    if scratch_flag:
        base_dir = dict_inputs["scratch_dir"]
    else:
        base_dir = dict_inputs["base_dir"]

    for i in list_iter:
        # "<base_dir>/<case_name>/<parlist>-<dm>/<case>-run_<iteration>"
        run_dirname = os.path.join(base_dir,
                                   dict_inputs["case_name"],
                                   "{}-{}" .format(
                                       dict_inputs["params_list_name"],
                                       dict_inputs["dm_name"]),
                                   "{}-run_{}" .format(
                                       dict_inputs["case_name"],
                                       str(i))
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
    p = subprocess.Popen(["hostname"], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    return p.communicate()[0].rstrip().decode("utf-8")


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    import sys

    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def parse_csv(csv_file) -> np.ndarray:
    """Parse a csv file, sniff the actual delimiter of the file

    This is used to load a generic csv file without specifying the actual
    delimiter

    **References:**
    stackoverflow.com/questions/16312104/python-import-csv-file-delimiter-or

    :param csv_file: the file of the csv file in string
    :return: a numpy array
    """
    import re
    
    output = list()

    lines = csv_file.readlines()
    for line in lines:
        output.append(re.split("\t|,| |;", line))

    output = np.array(output).astype(np.float)
    
    return output


def cmd_exists(cmd: str) -> bool:
    """Check if a command is available in the PATH

    Use shell command `which` to check whether an executable is in the path
    
    :param cmd: the name of the executable, assumed in the PATH
    :return: True if it is in the path, False otherwise
    """
    return subprocess.call("which " + cmd, shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE) == 0


def exe_exists(cmd: str) -> bool:
    """Check if a command is available in the specified path
    
    Use shell command `type` to check whether a file is an executable
    
    **Reference:**
    (1) Answer by `hasen`
       stackoverflow.com/questions/377017/test-if-executable-exists-in-python
    
    :param cmd: the name of the executable
    :return: True if such executable exists, False otherwise
    """
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE) == 0


def link_exec(executable: str, directory: str):
    """Create a symbolic link between an executable in a designated directory

    :param executable: the path to executable, either relative or absolute
    :param directory: the directory to create the symbolic link
    """
    import os

    # Get the absolute path
    abs_exec = os.path.abspath(executable)
    abs_dir = os.path.abspath(directory)

    # Create symbolic link
    subprocess.call(["ln", "-s", abs_exec, abs_dir])


def get_name(name: str, incl_ext: bool=False) -> str:
    """ Get the name of a directory of file, specified in path
    
    Path can either be relative or absolute
    
    :param name: the name of a directory or a file, specified in path
    :param incl_ext: flag to include the extension if it is a file
    :return: the name of the directory or the file, excluding path 
    """
    import os

    ext_delim = "."

    # Filter the directory delimiter and get the last element
    # It is assumed here that if it is a directory, it will not end with "/"
    name = os.path.split(name)[-1]
    if ext_delim in name:
        # Then it is a file with an extension
        if incl_ext:
            return name
        else:
            return name.split(ext_delim)[0]
    else:
        # Then it is a directory
        return name
