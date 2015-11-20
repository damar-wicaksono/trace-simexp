"""Module to prepare and execute extraction of variables from the dmx to a csv
"""

__author__ = "Damar Wicaksono"


def run(aptplot_executable: str, trace_vars: list,
        run_names: list, run_dirnames: list, info_filename:str):
    """Function to execute the aptplot in batch mode to extract trace variables
    """
    import subprocess
    import time

    from . import aptscript

    def done(p):
        return p.poll() == 0

    def success(p):
        return p.returncode == 0

    processes = list()

    # Open the exec.info file to be appended
    info_file = open(info_filename, "a")

    # Loop over the runs in the batch and create an aptplot process
    for run_name, run_dirname in zip(run_names, run_dirnames):

        # Create a string of apt command
        apt_script = aptscript.make_apt(run_name, trace_vars)

        # Write the aptscript into a temporary files
        apt_script_filename = "{}.apt" .format(run_name)
        apt_script_fullname = "{}/{}" .format(run_dirname, apt_script_filename)
        with open(apt_script_fullname, "w") as apt_script_file:
            for line in apt_script:
                apt_script_file.writelines("{}\n" .format(line))

        # Create a process and collect them in a list
        process = subprocess.Popen(
            [aptplot_executable, "-batch", apt_script_filename, "-nowin"], 
            cwd=run_dirname
        )
        processes.append(process)

    # Loop over processes and wait for them to finish
    while True:
        for i, process in enumerate(processes):
            try:
                process.wait(timeout=8000)
            except subprocess.TimeoutExpired:
                process.kill()

            if done(process):
                if not success(process):
                    info_file.writelines("Execution Failed: {}\n"
                        .format(subprocess.list2cmdline(process.args)))
                else:
                    info_file.writelines("Execution Successful: {}\n"
                        .format(subprocess.list2cmdline(process.args)))

                processes.remove(process)

        if not processes:
           break
        else:
           time.sleep(0.05)

    # Close the appended exec.info file
    info_file.close()
   
