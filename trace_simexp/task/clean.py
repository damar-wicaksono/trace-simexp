# -*- coding: utf-8 -*-
"""
    trace_simexp.task.clean
    ***********************

    Module to clean up files and directories contents
"""

__author__ = "Damar Wicaksono"


def rm_files(files: list):
    """Remove the listed files

    :param csv_files: the list files or directories, fullname
    """
    import subprocess
    import os

    for file in files:
        if os.path.isfile(file):
            subprocess.call(["rm", file])
        elif os.path.islink(file):
            subprocess.call(["rm", file])
        elif os.path.isdir(file):
            subprocess.call(["rm", "-rf", file])


def rm_except(directories: list, files: list):
    """Remove the all the directory contents except a single file

    :param directories: the list of directories
    :param files: files within the directories not to be deleted
    """
    import subprocess

    for directory, file in zip(directories, files):
        tmp_script = "find '{}' ! -name {} -type f -delete" .format(directory,
                                                                    file)
        # Use the whole string with shell interpreter
        subprocess.call(tmp_script, shell=True)
