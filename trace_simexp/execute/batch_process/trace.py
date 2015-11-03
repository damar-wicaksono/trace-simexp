"""Module to execute trace jobs sequentially
"""

__author__ = "Damar Wicaksono"


def run(run_dirnames: list, trace_commands: list, log_files: list):
    r"""

    :param run_dirnames:
    :param scratch_dirnames:
    :param trace_commands:
    :param log_files:
    :return:
    """
    import subprocess
    import time

    if not trace_commands:
        return

    def done(p):
        return p.poll() == 0

    def success(p):
        return p.returncode == 0

    processes = []

    while True:
        while trace_commands:
            task = trace_commands.pop(0)
            log_file = open(log_files.pop(0), "wt")
            run_dirname = run_dirnames.pop(0)
            processes.append(
                subprocess.Popen(task, stdout=log_file, cwd=run_dirname))

        for process in processes:
            try:
                process.wait(timeout=8000)
            except subprocess.TimeoutExpired:
                process.kill()

            if done(process):
                if success(process):
                    log_file.close()
                    processes.remove(process)
                else:
                    log_file.write("TRACE execution is killed - TimeOutError")
                    log_file.close()
                    processes.remove(process)

        if not processes:
            break
        else:
            time.sleep(0.05)


def link_xtv(run_dirnames: list,
             scratch_dirnames: list,
             scratch_xtvs: list):
    """

    :param run_dirnames:
    :param scratch_dirnames:
    :return:
    """
    import subprocess
    import os

    for scratch_dirname in scratch_dirnames:

        if not os.path.exists(scratch_dirname):
            os.makedirs(scratch_dirname)

    for scratch_xtv, run_dirname in zip(scratch_xtvs, run_dirnames):
        subprocess.call(["ln", "-s", scratch_xtv, run_dirname])