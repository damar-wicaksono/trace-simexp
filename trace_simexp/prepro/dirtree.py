"""Module to create a directory structures with the input files
"""

__author__ = "Damar Wicaksono"

HEADER_DIRNAME = "simulation"


def create(params_dict, str_template, dm, case_name, params_list_name,
           dm_name, samples,
           overwrite=False):
    r"""Create a directory structure for the simulation campaign

    :param params_dict: (list of dict) the list of parameters
    :param str_template: (str template) the template based on base tracin
    :param dm: (ndArray) the numpy array
    :param case_name: (str) the name of the case
    :param params_list_name: (str) the name of the list of parameters file
    :param dm_name: (str) the name of the design matrix
    :param samples: (list) the list of samples to be created
    :return:
    """
    import os
    from . import tracin

    # Create directory path name
    case_name_dir = "./{}/{}" .format(HEADER_DIRNAME, case_name)
    dm_name_dir = "{}/{}-{}" .format(case_name_dir, params_list_name, dm_name)

    if not os.path.exists(dm_name_dir):
        os.makedirs(dm_name_dir)

    # Loop over required samples
    for i in samples:
        num_runs = i + 1        # offset 1 for zero index list
        run_dir_name = "{}/{}-run_{}" .format(dm_name_dir, case_name, num_runs)

        if not os.path.exists(run_dir_name):
            os.makedirs(run_dir_name)

        str_tracin = tracin.create(str_template, params_dict, dm[i, :])
        tracin_filename = "{}-run_{}.inp" .format(case_name, num_runs)
        tracin_fullname = "{}/{}" .format(run_dir_name, tracin_filename)

        if os.path.isfile(tracin_fullname):
            if overwrite:
                with open(tracin_fullname, "wt") as tracin_file:
                    tracin_file.write(str_tracin)
            else:
                print("{} exist - no overwrite option" .format(tracin_fullname))
        else:
            with open(tracin_fullname, "wt") as tracin_file:
                    tracin_file.write(str_tracin)

def check(case_name, param_list_name, dm_name, samples):
    """

    :param case_name:
    :param dm_name:
    :param samples:
    :return:
    """
    import os

    # Create directory path name
    case_name_dir = "./{}/{}" .format(HEADER_DIRNAME, case_name)
    dm_name_dir = "{}/{}" .format(case_name_dir, dm_name)

    print("********************************")
    print("Checking Directory Structures...")
    print("********************************")

    if os.path.exists(dm_name_dir):
        print("Simulation Case directory: {} exists"
              .format(dm_name_dir))
        print("\n")
    else:
        print("Simulation Case directory: {} does not exist"
              .format(dm_name_dir))
        print("\n")

    print("************************")
    print("Checking input files...")

    for i in samples:
        num_runs = i+1
        run_dir_name = "{}/{}_run_{}" .format(dm_name_dir, case_name, num_runs)

        if os.path.exists(run_dir_name):

            print("*********")
            print("Case Name - {} Design Matrix - {}.inp"
                  .format(case_name, dm_name))

            tracin_filename = "{}_run_{}.inp" .format(case_name, num_runs)
            tracin_fullname = "{}/{}" .format(run_dir_name, tracin_filename)

            if os.path.isfile(tracin_fullname):
                print("Sample - {}. Full path - {}" .format(num_runs,
                                                            tracin_fullname))