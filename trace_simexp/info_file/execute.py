__author__ = 'wicaksono_d'


def read(info_filename: str):
    """Read the exec.info file produced in the execution phase

    :param info_filename: (str) the fullname of the exec.info file
    """

    # Read file
    with open(info_filename, "rt") as info_file:
        info_lines = info_file.read().splitlines()

    for num_line, line in enumerate(info_lines):

        if "prepro.info Filename" in line:
            prepro_info = line.split("-> ")[-1].strip()

        # Samples to run
        if "Samples to Run" in line:
            samples = []
            i = num_line + 1
            while True:
                if "***" in info_lines[i]:
                    break
                samples.extend([int(_) for _ in info_lines[i].split()])
                i += 1

    return prepro_info, samples