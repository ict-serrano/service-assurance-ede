import subprocess
from rq import get_current_job
import os


def ede_handler(config_path):
    job = get_current_job()
    job.meta['progress'] = "Started inference"
    job.save_meta()
    os.chdir("..")
    ede_exec = os.path.join(os.path.abspath(os.curdir), 'ede.py')
    subprocess.Popen(['python', ede_exec, '-f', config_path])
    job.meta['progress'] = "Finished inference"
    job.save_meta()
