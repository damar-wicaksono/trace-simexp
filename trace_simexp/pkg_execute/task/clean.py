"""Module to clean up unnecessary files after each batch execution
"""

__author__ = "Damar Wicaksono"


def run(list_files: list):
    """Remove unnecessary files after each batch execution of TRACE

    :param list_files: the list of file fullnames to be removed
    :return: - 
    """
    import subprocess
    import os
    
    for in_file in list_files:
        if os.path.isfile(in_file):
            subprocess.call(["rm", in_file])
        elif os.path.islink(in_file):
            subprocess.call(["rm", in_file])
        