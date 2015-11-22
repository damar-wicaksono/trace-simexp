import numpy as np

from trace_simexp import postpro

__author__ = "Damar Wicaksono"

from trace_simexp import postpro

def main():

    # Consolidate all the required inputs for post-processing phase
    postpro_inputs = postpro.get_input()

    # Commence the conversion
    postpro.dmx2csv(postpro_inputs)


if __name__ == "__main__":
    main()

