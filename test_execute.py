import numpy as np

from trace_simexp import pkg_execute

__author__ = "Damar Wicaksono"


def main():

    # Prototypical user inputs for preprocessing phase
    exec_inputs = pkg_execute.input.get()

    pkg_execute.batches.run(exec_inputs)


if __name__ == "__main__":
    main()