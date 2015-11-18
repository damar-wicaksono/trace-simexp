import numpy as np

from trace_simexp import prepro

__author__ = "Damar Wicaksono"


def main():

    # Prototypical user inputs for preprocessing phase
    inputs = prepro.input.get()

    # The preprocessing step

    # 1.a. Read list of parameters file and create a dictionary from it
    params_dict = prepro.paramfile.inp_to_dict(inputs["params_list_file"],
                                               inputs["info_file"])

    # 1.b. Read the base tracin file and obtain the nominal values
    prepro.template.get_nominal_values(inputs["tracin_base_file"], params_dict)

    # 2. Create a string template
    str_template = prepro.template.create(params_dict,
                                          inputs["tracin_base_file"])

    # 3. Read Design Matrix into a numpy array
    dm = np.loadtxt(inputs["dm_file"])

    # 4. Create a directory structure based on
    prepro.dirtree.create(params_dict, str_template, dm,
                          inputs["case_name"],
                          inputs["params_list_name"],
                          inputs["dm_name"],
                          inputs["base_name"],
                          inputs["samples"],
                          inputs["overwrite"])


if __name__ == "__main__":
    main()