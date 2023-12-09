import subprocess
from rq import get_current_job
import os
import time
from service_utils import check_pid, save_pid

def ede_log_handler(ede_log,
                    job,
                    pid):
    ede_log.seek(0, os.SEEK_END)

    # start read loop
    while True:
        line = ede_log.readline()
        try:
            if not line:
                time.sleep(1)
                job.meta['progress'] = "Waiting for log to start"
                job.save_meta()
                continue
        except Exception as e:
            job.meta['progress'] = "Error reading log file"
            job.save_meta()
            continue
        job.meta['progress'] = line.strip()
        job.save_meta()
        if check_pid(pid) == 0:
            break

def ede_pid_handler(job_id, ede_pid):
    watch_dog_file = 'ede_{}.pid'.format(job_id)
    save_pid(ede_pid, watch_dog_file)

def ede_handler(config_path):
    job = get_current_job()
    job.meta['progress'] = "Started inference"
    job.save_meta()
    if os.getcwd().split('/')[-1] == 'service':  # TODO fix this
        os.chdir("..")
    ede_exec = os.path.join(os.path.abspath(os.curdir), 'ede.py')

    exec = subprocess.Popen(['python', ede_exec, '-f', config_path])
    ede_pid_handler(job.get_id(), exec.pid)
    ede_log = open(os.path.join(os.path.abspath(os.curdir), 'ede.log'), 'r')
    ede_log_handler(ede_log, job, exec.pid)
    job.get_id()
    job.meta['progress'] = "Finished inference"
    job.save_meta()
