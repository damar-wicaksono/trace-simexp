# -*- coding: utf-8 -*-
"""
    trace_simexp.task.xtv2dmx
    *************************

    Module to execute XTV2DMX tasks simultaneously for task within a batch and
    sequentially between batches
"""

__author__ = "Damar Wicaksono"


def run(xtv2dmx_commands: list, log_files: list, 
        run_dirnames: list, info_filename: str):
    """Submit multiple xtv to dmx conversion jobs and wait until finish
    
    :param xtv2dmx_commands: list of xtv2dmx shell commands
    :param log_files: list of log fullnames
    :param run_dirnames: list of run directory names, 
        used as the working directory for the shell command execution
    :param info_filename: (str) the exec.info file to be appended
    """
    import subprocess
    import time
    
    # Preserve some lists for re-use
    run_dirnames_cp = run_dirnames.copy()
    log_files_cp = log_files.copy()
    
    if not xtv2dmx_commands:
        return
    
    def done(p):
        return p.poll() == 0

    def success(p):
        return p.returncode == 0
        
    processes = []

    # Open the exec.info file to be appended
    info_file = open(info_filename, "a")
    
    while True:
        # Submit all the jobs
        while xtv2dmx_commands:
            
            # Loop over all the passed arguments
            task = xtv2dmx_commands.pop(0)
            log_file = open(log_files_cp.pop(0), "at")
            run_dirname = run_dirnames_cp.pop(0)
            
            # Create a process and collect them in a list
            process = subprocess.Popen(task, 
                                       stdout=log_file, 
                                       stderr=log_file, 
                                       cwd=run_dirname)
            processes.append(process)
            
            # Make some description in the log file
            log_file.write("###\n")
            log_file.write("Executing: {}\n" 
                .format(subprocess.list2cmdline(process.args)))
            
        # Loop over process and wait for them to finish
        for process in processes:
            try:
                process.wait(timeout=8000)
            except subprocess.TimeoutExpired:
                process.kill()
            
            if done(process):
                if not success(process):
                    log_file.write("XTV2DMX Conversion failed")
                    info_file.writelines("Execution Failed: {}\n"
                        .format(subprocess.list2cmdline(process.args)))
                else:
                    info_file.writelines("Execution Successful: {}\n"
                        .format(subprocess.list2cmdline(process.args)))

                log_file.close()
                processes.remove(process)
    
        if not processes:
            break
        else:
            time.sleep(0.05)

    # Close the appended exec.info file
    info_file.close()
    

def make_commands(xtv2dmx_executable: str,
                  xtv_filenames: list,
                  dmx_filenames: list) -> list:
    """Create list of shell command to convert xtv files into dmx files
    
    The conversion includes compression to reduce space requirements

    :param xtv2dmx_executable: the name of the xtv2dmx executable
    :param xtv_filenames: the list of xtv filenames to be converted
    :param dmx_filenames: the list of dmx filenames as target output
    :return: a list of xtv2dmx shell command to be executed
    """
    xtv2dmx_commands = []
    
    for xtv_filename, dmx_filename in zip(xtv_filenames, dmx_filenames):
        xtv2dmx_command = [xtv2dmx_executable,
                           "-r", xtv_filename, 
                           "-d", dmx_filename]
        xtv2dmx_commands.append(xtv2dmx_command)
    
    return xtv2dmx_commands
    
    
def link_dmx(run_dmxs: list, scratch_dmxs: list):
    """Create a soft link between rundir dmx and scratchdir dmx
    
    :param run_dmxs: list of dmx fullname in the run directory
    :param scratch_dmxs: list of dmx fullname in the scratch directory
    :return: -
    """
    import subprocess
    import os
    
    for run_dmx, scratch_dmx in zip(run_dmxs, scratch_dmxs):
        
        # Delete file and link if they exist
        if os.path.islink(run_dmx):
            subprocess.call(["rm", "-f", run_dmx])
        if os.path.isfile(scratch_dmx):
            subprocess.call(["rm", "-f", scratch_dmx])
        
        subprocess.call(["ln", "-s", scratch_dmx, run_dmx])
