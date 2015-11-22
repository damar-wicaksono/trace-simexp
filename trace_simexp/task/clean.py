"""Module to reset to each of the phases
"""

__author__ = "Damar Wicaksono"


def rm_files(files: list):
    """Remove the listed files

    :param csv_files: (list) the list files, fullname
    """
    import subprocess
    import os

    for file in files:
        if os.path.isfile(file):
            subprocess.call(["rm", file])
        elif os.path.islink(file):
            subprocess.call(["rm", file])


def rm_except(directories: list, files: list):
    """Remove the all the directory contents except the files

    :param directories:
    :param files:
    """
    import subprocess

    for directory, file in zip(directories, files):
        subprocess.call(["find", directory, "! -name", file,
                         "-type f", "-delete"])
