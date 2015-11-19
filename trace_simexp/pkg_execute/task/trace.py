"""Module to execute TRACE tasks simultaneously for task within a batch 
and sequentially between batches.
"""

__author__ = "Damar Wicaksono"


def run(trace_commands: list, log_files: list, 
        run_dirnames: list, info_filename: str):
    """Submit multiple trace jobs and wait until finish

    :param trace_commands: the list of trace shell commands
    :param log_files: the list of logfullnames
    :param run_dirnames: list of run directory names,
        used as the working directory for the shell command execution
    :return: - 
    """
    import subprocess
    import time

    # Preserve some lists for re-use
    run_dirnames_cp = run_dirnames.copy()
    log_files_cp = log_files.copy()
    
    if not trace_commands:
        return

    def done(p):
        return p.poll() == 0

    def success(p):
        return p.returncode == 0

    processes = []

    # Open the info filename to be appended
    info_file = open(info_filename, "a")

    while True:
        while trace_commands:
            
            # Loop over all the passed arguments
            task = trace_commands.pop(0)
            log_file = open(log_files_cp.pop(0), "wt")
            run_dirname = run_dirnames_cp.pop(0)
            
            # Create a process and collect them in a list
            process = subprocess.Popen(task, stdout=log_file, cwd=run_dirname)
            processes.append(process)
            
            # Make some description in the log file
            log_file.write("###\n")
            log_file.write("Executing: {}\n" 
                .format(subprocess.list2cmdline(process.args)))
        
        # Loop over process and wait them to finish    
        for process in processes:
            try:
                process.wait(timeout=8000)
            except subprocess.TimeoutExpired:
                process.kill()

            if done(process):
                if not success(process):
                    log_file.write("TRACE execution is killed - TimeOutError")
                    info_file.writelines("Execution Failed: {}\n"
                              .format(subprocess.list2cmdline(process.args)))
                else:
                    info_file.writelines("Execution Successfull: {}\n"
                              .format(subprocess.list2cmdline(process.args)))
                log_file.close()
                processes.remove(process)

        if not processes:
            break
        else:
            time.sleep(0.05)

    # Close the info file 
    info_file.close()


def make_commands(exec_inputs: dict, tracin_filenames: list) -> list:
    """Create a list of shell command to run trace on the supplied set of tracin

    :param exec_inputs: the dictionary with parameters for execute phase
    :param tracin_filenames: the list of trace input file to be simulated
    :return: a list of trace shell command to be executed
    """
    trace_commands = []

    for tracin_filename in tracin_filenames:
        trace_command = [exec_inputs["trace_exec"], "-p", tracin_filename]
        trace_commands.append(trace_command)

    return trace_commands
    
    
def link_xtv(scratch_dirnames: list, run_xtvs: list, scratch_xtvs: list):
    """Create a soft link between xtv in the run directories and in the scratch

    The actual xtv file is located in the scratch to save space in the more 
    limited activity folder
    
    :param scratch_dirnames: the list of the scratch directory names, 
        will be created if they do not exist 
    :param run_xtvs: the list of xtv fullnames in the run directory
    :param scratch_xtvs: the list of xtv fullnames in the scratch
    :return: -
    """
    import subprocess
    import os

    for scratch_dirname in scratch_dirnames:

        if not os.path.exists(scratch_dirname):
            os.makedirs(scratch_dirname)

    for scratch_xtv, run_xtv in zip(scratch_xtvs, run_xtvs):
        if os.path.isfile(scratch_xtv):
            subprocess.call(["rm", "-f", scratch_xtv])
        if os.path.islink(run_xtv):
            subprocess.call(["rm", "-f", run_xtv])
            
        subprocess.call(["ln", "-s", scratch_xtv, run_xtv])

