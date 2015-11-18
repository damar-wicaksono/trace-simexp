# `trace_simexp`: Executing TRACE

The package `trace_simexp` is responsible for executing the generated TRACE
input deck from the design matrix. 
The analyst is required to specify the following information to the procedure

 1. `case_name`: The case name of the simulation experiment
 2. `dm_name`: The design matrix name of the simulation experiment
 3. `samples`: Provided that such sample(s) exists, the samples can be provided
    as a list, as a selection separated by comma, or a single sample
 4. `num_procs`: The number of processors
 5. `trace_executable`: The executable of TRACE
 6. `xtv2dmx_executable`: The executable of xvt2dmx
 7. `scratch_dir`: The scratch directory
 
The first 2 arguments provide connection with the previous step of
pre-processing. However, there is still no connection made to the actual list
of parameters file: `case_name` and `dm_name` are suffice for the script to
look into the directory structures. How to uniquely specify a directory structures based on:
 
 1. `case_name`: the base tracin filename (recommended, excl. the extension)
 2. `dm_name`: the design matrix filename (excl. the extension)
 3. `params_list_name`: the list of parameters filename (excl. the extension)
 
is still under consideration.

For flexibility only `samples` are available to the user via the command line
argument, while the other has to be specified in the driver script.

The process of trace execution is:

 1. Take user input
 2. Check the directory structures, check the scratch dir, check the executables
 3. Create a batch runs according to the number of processors and # of samples
 4. Execute TRACE
 5. Convert the xtv to dmx
 6. Remove unnecessary files
 7. Create report: put date, the case name, the samples, the executable, etc.