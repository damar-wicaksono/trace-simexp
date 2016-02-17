import numpy as np

from trace_simexp import execute

__author__ = "Damar Wicaksono"


def main():

    # Consolidate all the required inputs for post-processing phase
    exec_inputs = execute.get_input()

    # Commence the conversion
    execute.run_batches(exec_inputs)

    # Revert back to execute phase state
    # execute.reset(exec_inputs)


if __name__ == "__main__":
    main()
