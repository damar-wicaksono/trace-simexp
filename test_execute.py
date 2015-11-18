import numpy as np

from trace_simexp import execute

__author__ = "Damar Wicaksono"


def main():

    # Prototypical user inputs for preprocessing phase
    exec_inputs = execute.input.get()

    execute.batches.run(exec_inputs)


if __name__ == "__main__":
    main()