"""Module to prepare and execute extraction of variables from the dmx to a csv
"""

__author__ = "Damar Wicaksono"


def run(aptplot_executable: str, 
        xtv_vars: list, xtv_vars_name:str,
        run_names: list, run_dirnames: list, 
        info_filename: str):
    """Function to execute the aptplot in batch mode to extract trace variables

    :param aptplot_executable: the fullname of aptplot executable
    :param xtv_vars: the list of TRACE graphic variables to be extracted
    :param xtv_vars_name: the name of the list of graphic variables file
    :param run_names: The run names = case_name + sample_num
    :param run_dirnames: the run directory names, relative to driver script
    :param info_filename: the postpro.info file to be appended
    """
    import os
    import subprocess
    import time

    from . import aptscript

    def done(p):
        return p.poll() == 0

    def success(p):
        return p.returncode == 0

    processes = list()
    apt_script_files = list()

    # Open the exec.info file to be appended
    info_file = open(info_filename, "a")

    # Loop over the runs in the batch and create an aptplot process
    for run_name, run_dirname in zip(run_names, run_dirnames):

        # Create a string of apt command
        apt_script = aptscript.make_apt(run_name, xtv_vars_name, xtv_vars)

        # Write the aptscript into a temporary files
        apt_script_filename = "{}-{}.apt" .format(run_name, xtv_vars_name)
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

        # Create list of files to be cleanup later
        apt_script_files.append(apt_script_fullname)

    # Loop over processes and wait for them to finish
    while True:
        for i, process in enumerate(processes):
            cmd_str = subprocess.list2cmdline(process.args)  # the string cmd
            try:
                process.wait(timeout=8000)
            except subprocess.TimeoutExpired:
                process.kill()

            if done(process):
                if not success(process):
                    info_file.writelines("Execution Failed: {}\n"
                                         .format(cmd_str))
                else:
                    info_file.writelines("Execution Successful: {}\n"
                                         .format(cmd_str))

                # remove the process
                processes.remove(process)

        if not processes:
            break
        else:
            time.sleep(0.05)

    # Clean up temporary aptscript file
    for apt_script_file in apt_script_files:
        os.remove(apt_script_file)

    # Close the appended exec.info file
    info_file.close()
