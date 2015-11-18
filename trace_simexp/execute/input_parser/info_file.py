"""Module to read pre-processing info file - Execute phase
"""

__author__ = "Damar Wicaksono"


def prepro_read(info_fullname: str):
    r"""Read the info file produced in the pre-processing phase

    :param info_fullname: (str) the fullname of the pre-pro info file
    :return:
    """

    # Read file
    with open(info_fullname, "rt") as info_file:
        info_lines = info_file.read().splitlines()

    # Loop over lines to obtain the parameter
    for num_line, line in enumerate(info_lines):

        # Base Directory
        if "Base Directory Name" in line:
            base_dir = line.split("-> ")[-1].strip()

        # Base Case Name
        if "Base Case Name" in line:
            case_name = line.split("-> ")[-1].strip()

        # List of parameters name
        if "List of Parameters Name" in line:
            params_list_name = line.split("-> ")[-1].strip()

        # Design Matrix filename
        if "Design Matrix Name" in line:
            dm_name = line.split("-> ")[-1].strip()

        # Samples to run
        if "Samples to Run" in line:
            samples = []
            i = num_line + 1
            while True:
                if "***" in info_lines[i]:
                    break
                samples.extend([int(_) for _ in info_lines[i].split()])
                i += 1

    return base_dir, case_name, params_list_name, dm_name, samples


def execute_write(info_filename):
    """

    :param info_filename:
    :return:
    """
