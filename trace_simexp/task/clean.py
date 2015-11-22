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
