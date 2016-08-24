import numpy as np

from trace_simexp import prepro
from trace_simexp import tracin
from trace_simexp import util

__author__ = "Damar Wicaksono"


def main():

    # Construct a dictionary of required inputs from command line arguments, etc
    inputs = prepro.get_input()

    # Read list of parameters file and create a dictionary from it
    params_dict = prepro.read_params(inputs["params_list_file"],
                                     inputs["info_file"],
                                     inputs["tracin_base_file"])

    # Create a string template
    tracin_template = tracin.create_template(params_dict,
                                             inputs["tracin_base_file"])

    # Read Design Matrix into a numpy array
    dm = util.parse_csv(inputs["dm_file"])

    # Create a directory structure based on the specified input
    prepro.create_dirtree(inputs, params_dict, tracin_template, dm)


if __name__ == "__main__":
    main()
