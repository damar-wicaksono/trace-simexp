"""Module to execute XTV2DMX tasks simultaneously for task within a batch
and sequentially between batches.
"""

__author__ = "Damar Wicaksono"


def run(xtv2dmx_commands: list, log_files: list, run_dirnames: list):
    """Submit multiple xtv to dmx conversion jobs and wait until finish
    
    :param xtv2dmx_commands: list of xtv2dmx shell commands
    :param log_files: list of log fullnames
    :param run_dirnames: list of run directory names, 
        used as the working directory for the shell command execution
    :return: -
    """
    import subprocess
    import time
    
    if not xtv2dmx_commands:
        return
    
    def done(p):
        return p.poll() == 0

    def success(p):
        return p.returncode == 0
        
    processes = []
    
    while True:
        # Submit all the jobs
        while xtv2dmx_commands:
            
            # Loop over all the passed arguments
            task = xtv2dmx_commands.pop(0)
            log_file = open(log_files.pop(0), "at")
            run_dirname = run_dirnames.pop(0)
            
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
                log_file.close()
                processes.remove(process)
    
        if not processes:
            break
        else:
            time.sleep(0.05)
    
    
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
        if os.path.isfile(run_dmx):
            subprocess.call(["rm", "-f", run_dmx])
        if os.path.isfile(scratch_dmx):
            subprocess.call(["rm", "-f", scratch_dmx])
        
        subprocess.call(["ln", "-s", scratch_dmx, run_dmx])
        
    