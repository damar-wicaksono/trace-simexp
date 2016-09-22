"""Driver script to compile all the csv files from TRACE campaign given dm file
"""
import argparse
import joblib
import os
import numpy as np
import tables as tb

import trace_simexp


__author__ = "Damar Wicaksono"


def get_inputs():
    """Get the command line args to collect a directory tree of TRACE to HDF5
    """
    parser = argparse.ArgumentParser(description="Compile TRACE runs to HDF5")
    # The postpro info filename
    parser.add_argument("-postpro" , "--postpro_info", type=str,
                        help="The postpro phase info file",
                        required=True)
    # The number of processors (compiling runs involve interpolation)
    parser.add_argument("-nprocs", "--num_procs", type=int,
                        help="The number of processors",
                        required=False,
                        default=1)
    # The end time in the interpolation of time-dependent data
    parser.add_argument("-tend", "--end_time", type=float,
                        help="The end time in interpolated data in [s]",
                        required=True)
    # The total number of axial locations
    parser.add_argument("-naxl", "--num_axial", type=int,
                        help="The total number of axial location",
                        required=True)
    # The time step size
    parser.add_argument("-tstep", "--t_delta", type=float,
                        help="The time step size in [s]",
                        required=False,
                        default=0.1)

    args = parser.parse_args()

    return args.postpro_info, args.num_procs, args.end_time, \
        args.t_delta, args.num_axial


def unify_time(time_data, var_data, t_max, t_delta):
    """Create a uniform time-step from an arbitrary time-dependent data"""
    from scipy import interpolate

    unif_time = np.arange(0.0, t_max, t_delta)

    tck = interpolate.splrep(time_data, var_data, s=0)
    unif_var_data = interpolate.splev(unif_time, tck, der=0)

    return unif_var_data


def interpolate_trace(csv_fullname: str, t_end: float, t_step: float, n_ax:int):
    """Create time-dependent temperature as a function of axial location
    
    The time-dependent data from raw trace output is interpolated into 
    a uniform time grid for consistent downstream analysis (different
    parameter values in a parameter perturbation campaign might result
    in different adaptive time-step size that is hard to control a priori)
    
    The final data structure resembles an "image" with instantaneous 
    temperature written column-wise, in different axial locations row-wise
        
    The function is specifically used to post-process a statistical 
    parameter perturbation campaign resulting in multiple realizations of 
    1D reflood TRACE transient simulation output
    
    The first column of the raw csv is assumed to be the time, the next
    `n_ax` columns is the axial location, and the next `n_ax` is the 
    time-dependent temperature at different axial locations
        
    :param csv_fullname: the fullname of post-processed csv file
    :param t_end: the end of transient
    :param t_step: the time step size of a uniform data
    :param n_ax: the number of axial location
    :return: the unified data in numpy array (row = time, column = ax. loc.)
    """
    
    # Read the raw data
    data = np.loadtxt(csv_fullname, 
                      skiprows=2, dtype=bytes, delimiter=",").astype("float")
    # Unify the time grid
    unif_data = unify_time(data[:, 0], data[:, n_ax+1], t_end, t_step)
    for j in range(n_ax+2, 2*n_ax+1):
        # Loop over each axial location and append the array
        unif_data = np.column_stack((unif_data,
                                    unify_time(data[:, 0], data[:, j], 
                                               t_end, t_step)))
    
    return unif_data.T
    

def get_axlocs(csv_fullname: str, n_axl: int):
    """Get the axial locations in [m] from the csv file
    
    :param csv_fullname:
    :param n_axl:
    :return: 
    """
    # Read the raw data
    data = np.loadtxt(csv_fullname, 
                      skiprows=2, dtype=bytes, delimiter=",").astype("float")
    # Get the axial location (in [m])
    return data[0, 1:(n_axl+1)]
    
    
def parallel_procs(n_jobs: int, n_procs: int, 
                   csv_files: list, t_end: float, t_step: float, n_ax: int):
    """Wrapper for naively parallel for loop implementation using joblib package
    
    :param n_jobs: total number of jobs to process
    :param n_procs: the number of processors
    :param csv_files: the list of csv fullname to (post)-post-process
    :param t_end: the end time
    :param t_step: the time step size
    """
    paralellizer = joblib.Parallel(n_procs)
    task_iterator = (joblib.delayed(interpolate_trace)(csv_files[i], t_end, 
                                                       t_step, n_ax)\
                                                        for i in range(n_jobs))
                                                        
    # Combine the results
    results = paralellizer(task_iterator)

    return results


def main():
    """Main entry point for the script"""

    # Get the command line arguments
    postpro_infofile, num_procs, t_end, t_delta, num_axial = get_inputs()
    
    # Construct the run directory name and aptplot name
    campaign_name, runs_directory, apt_name = \
        trace_simexp.info_file.postpro.read(postpro_infofile)
    
    # Parse the run directory and check if all the csv files exist
    csv_files = []
    for run_dir in os.listdir(runs_directory):
        csv_filename = "{}-{}.csv" .format(run_dir, apt_name)
        csv_fullname = "{}/{}/{}" .format(runs_directory, run_dir, csv_filename)
        if not os.path.isfile(csv_fullname):
            raise ValueError("CSV file not found!")
        else:
            csv_files.append(csv_fullname)
            
    n_jobs = len(csv_files)         # The number of jobs/files to process
    
    # Prepare HDF5
    outfilename = "{}.h5" .format(campaign_name)
    outfile = tb.open_file(outfilename, "w")

    grp_run = outfile.create_group("/", "runs", campaign_name)

    results = parallel_procs(n_jobs, num_procs, csv_files, t_end, 
                             t_delta, num_axial)

    # Save uniform time to the hdf5 file
    unif_time = np.arange(0.0, t_end, t_delta)
    outfile.create_array("/", "time", unif_time)
    # Save the axial locations to the hdf5 file
    ax_locs = get_axlocs(csv_files[0], num_axial)
    outfile.create_array("/", "ax_locs", ax_locs)
    # Save the time-axial grid for easy plotting into the hdf5 file
    grid_time, grid_axial = np.meshgrid(unif_time, ax_locs)
    grp_grid = outfile.create_group("/", "grid", "the axial location and time grid")
    outfile.create_array(grp_grid, "grid_time", grid_time, "time grid")
    outfile.create_array(grp_grid, "grid_z", grid_axial, "z-axis grid")
    
    # Save the results into hdf5 file
    for i, result in enumerate(results):
        data_name = "run_{}" .format(i+1)
        outfile.create_array(grp_run, data_name, result)

    outfile.close()
