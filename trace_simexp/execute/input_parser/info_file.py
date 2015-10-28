"""Module to read info file - Execute phase
"""

__author__ = "Damar Wicaksono"


def prepro_read(info_filename):
    r"""Read the info file produced in the pre-processing phase

    :param info_filename: (str) the filename for the info_file
    :return:
    """

    # Read file
    with open(info_filename, "rt") as info_file:
        info_lines = info_file.read().splitlines()

    # Loop over lines to obtain the parameter
    for num_line, line in enumerate(info_lines):

        # Base Directory
        if "Base Directory Name" in line:
            base_dir = line.split("-> ")[-1]

        # Base Case Name
        if "Base Case Name" in line:
            case_name = line.split("-> ")[-1]

        # List of parameters name
        if "List of Parameters Name" in line:
            params_list_name = line.split("-> ")[-1]

        # Design Matrix filename
        if "Design Matrix Name" in line:
            dm_name = line.split("-> ")[-1]

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
