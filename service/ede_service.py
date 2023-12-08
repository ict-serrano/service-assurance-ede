"""

Copyright 2023, West University of Timisoara, Timisoara, Romania
Developers:
 * Gabriel Iuhasz, iuhasz.gabriel@info.uvt.ro

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at:
    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from flask import send_file
from flask import request
import os
import jinja2
import sys
import subprocess
import platform
from flask import send_from_directory, jsonify
from werkzeug.utils import secure_filename
import marshmallow
from flask_restful import Resource
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_apispec.annotations import doc
from app import *
from service_utils import *
import psutil
from redis import Redis
import rq
from rq.job import Job
from rq.command import send_stop_job_command
from rq import cancel_job
import glob



#directory locations
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')
models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../models')
conf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../conf')
etc_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'etc')
#file location

service_log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
log_file = os.path.join(service_log_dir, 'ede_service.log')

#Allowed extensions
ALLOWED_CONF_EXTENSIONS = {'yaml', 'yml'}
ALLOWED_MODEL_EXTENSIONS = {'pkl', 'joblib'}
ALLOWED_SCALER_EXTENSIONS = {'scaler', 'pkl', 'joblib'}
ALLOWED_DATA_EXTENSIONS = {'csv', 'tsv', 'txt', 'xlsx', 'xls'}

# redis connection
redis_end = os.getenv('REDIS_END', 'redis')
redis_port = os.getenv('REDIS_PORT', 6379)
r_name = os.getenv('RQ_NAME', 'edeservice')
r_connection = Redis(host=redis_end, port=redis_port)
queue = rq.Queue(r_name, connection=r_connection)

# Schemas
class EDEStatusSchema(marshmallow.Schema):
    status = marshmallow.fields.String(default='ok')
    python_version = marshmallow.fields.String()
    platform = marshmallow.fields.String()
    sklearn_version = marshmallow.fields.String()
    shap_version = marshmallow.fields.String()

@doc(description='EDE Status descriptor', tags=['status'])
@marshal_with(EDEStatusSchema, code=200)
class EDEStatus(Resource, MethodResource):
    def get(self):
        import sklearn, shap
        resp = jsonify({
            'status': 'ok',
            'python_version': sys.version,
            'platform': platform.platform(),
            'sklearn_version': sklearn.__version__,
            'shap_version': shap.__version__
        })
        resp.status_code = 200
        return resp


@doc(description='Global config for EDE', tags=['config'])
class Config(Resource, MethodResource):
    def get(self):
        try:
            conf = readConf(os.path.join(conf_dir, 'ede_config_service.yaml')) # todo list all configs make one active
        except Exception as e:
            return {'error': str(e)}, 500
        resp = jsonify(conf)
        log.info('Returned default config!')
        resp.status_code = 200
        return resp

    def put(self):
        if 'file' not in request.files:
            log.error('No file in request!')
            resp = jsonify(
                {
                    'error': 'no file in request'
                }
            )
            resp.status_code = 400
            return resp
        file = request.files['file']
        if file.filename == '':
            log.error('No file selected for upload')
            resp = jsonify(
                {
                    'message': 'no file selected for upload'
                }
            )
            resp.status_code = 400
        if file and allowed_file(file.filename, ALLOWED_CONF_EXTENSIONS):
            filename = secure_filename(file.filename)
            file.save(os.path.join(data_dir, filename))
            log.info(f"Data {file.filename} upload succesfull")
            resp = jsonify({
                'message': "data upload successfull"
            })
            resp.status_code = 201
        else:
            log.error(f"Unsupported data content_type, supported are {list(ALLOWED_CONF_EXTENSIONS)}")
            resp = jsonify(
                {
                    'message': f'allowed data file types are: {list(ALLOWED_CONF_EXTENSIONS)}'
                }
            )
            resp.status_code = 400
        return resp


@doc(description='Connector config for EDE', tags=['config'])
class ConnectorConfig(Resource, MethodResource):
    def get(self):
        try:
            conf = readConf(os.path.join(conf_dir, 'ede_config_service.yaml'))  # todo list all configs make one active
        except Exception as e:
            return {'error': str(e)}, 500
        resp = jsonify(conf['Connector'])
        log.info('Returned connector config!')
        resp.status_code = 200
        return resp

    def put(self):
        if request.is_json:
            try:
                conf = readConf(
                    os.path.join(conf_dir, 'ede_config_service.yaml'))  # todo list all configs make one active
            except Exception as e:
                return {'error': str(e)}, 500
            new_conf = replace_field(conf, 'Connector', request.json)
            yaml.dump(new_conf, open(os.path.join(conf_dir, 'ede_config_service.yaml'), 'w'))
            return jsonify(new_conf) # TODO validate request
        else:
            log.error('No json in request!')
            resp = jsonify(
                {
                    'error': 'no json in request'
                }
            )
            resp.status_code = 400
            return resp


@doc(description='Filter config for EDE', tags=['config'])
class FilterConfig(Resource, MethodResource):
    def get(self):
        try:
            conf = readConf(os.path.join(conf_dir, 'ede_config_service.yaml'))  # todo list all configs make one active
        except Exception as e:
            return {'error': str(e)}, 500
        resp = jsonify(conf['Filter'])
        log.info('Returned filter config!')
        resp.status_code = 200
        return resp

    def put(self):
        if request.is_json:
            try:
                conf = readConf(
                    os.path.join(conf_dir, 'ede_config_service.yaml'))  # todo list all configs make one active
            except Exception as e:
                return {'error': str(e)}, 500
            new_conf = replace_field(conf, 'Filter', request.json)
            yaml.dump(new_conf, open(os.path.join(conf_dir, 'ede_config_service.yaml'), 'w'))
            return jsonify(new_conf) # TODO validate request
        else:
            log.error('No json in request!')
            resp = jsonify(
                {
                    'error': 'no json in request'
                }
            )
            resp.status_code = 400
            return resp


@doc(description='Augmentation config for EDE', tags=['config'])
class AugmentationConfig(Resource, MethodResource):
    def get(self):
        try:
            conf = readConf(os.path.join(conf_dir, 'ede_config_service.yaml'))  # todo list all configs make one active
        except Exception as e:
            return {'error': str(e)}, 500
        resp = jsonify(conf['Augmentation'])
        log.info('Returned augmentation config!')
        resp.status_code = 200
        return resp

    def put(self):
        if request.is_json:
            try:
                conf = readConf(
                    os.path.join(conf_dir, 'ede_config_service.yaml'))  # todo list all configs make one active
            except Exception as e:
                return {'error': str(e)}, 500
            new_conf = replace_field(conf, 'Augmentation', request.json)
            yaml.dump(new_conf, open(os.path.join(conf_dir, 'ede_config_service.yaml'), 'w'))
            return jsonify(new_conf) # TODO validate request
        else:
            log.error('No json in request!')
            resp = jsonify(
                {
                    'error': 'no json in request'
                }
            )
            resp.status_code = 400
            return resp


@doc(description='Inference config for EDE', tags=['config'])
class InferenceConfig(Resource, MethodResource):
    def get(self):
        try:
            conf = readConf(os.path.join(conf_dir, 'ede_config_service.yaml'))  # todo list all configs make one active
        except Exception as e:
            return {'error': str(e)}, 500
        resp = jsonify(conf['Detect'])
        log.info('Returned inference config!')
        resp.status_code = 200
        return resp

    def put(self):
        if request.is_json:
            try:
                conf = readConf(
                    os.path.join(conf_dir, 'ede_config_service.yaml'))  # todo list all configs make one active
            except Exception as e:
                return {'error': str(e)}, 500
            new_conf = replace_field(conf, 'Detect', request.json)
            yaml.dump(new_conf, open(os.path.join(conf_dir, 'ede_config_service.yaml'), 'w'))
            return jsonify(new_conf) # TODO validate request
        else:
            log.error('No json in request!')
            resp = jsonify(
                {
                    'error': 'no json in request'
                }
            )
            resp.status_code = 400
            return resp


# ############## Control #################
@doc(description='Fetch EDE Logs', tags=['logs'])
class EDELogs(Resource, MethodResource):
    def get(self):
        return send_file(log_file, mimetype='text/plain')


@doc(description='List local data', tags=['data'])
class LocalData(Resource, MethodResource):
    def get(self):
        files = os.listdir(data_dir)
        for f in files:
            if not allowed_file(f, ALLOWED_DATA_EXTENSIONS):
                files.remove(f)
        return jsonify({'files': files})


@doc(description='Handler for local data', tags=['data'])
class LocalDataHandler(Resource, MethodResource):
    def get(self, data_file):
        return send_from_directory(data_dir, data_file)

    def put(self, data_file):

        if 'file' not in request.files:
            log.error('No file in request!')
            resp = jsonify(
                {
                    'error': 'no file in request'
                }
            )
            resp.status_code = 400
            return resp
        file = request.files['file']
        if file.filename == '':
            log.error('No file selected for upload')
            resp = jsonify(
                {
                    'message': 'no file selected for upload'
                }
            )
            resp.status_code = 400
        if file and allowed_file(file.filename, ALLOWED_DATA_EXTENSIONS):
            filename = secure_filename(file.filename)
            if data_file != filename:
                log.error(f"File name in request {data_file} does not match file name in data {filename}")
                resp = jsonify(
                    {
                        'message': f'file name in request {data_file} does not match file name in data {filename}'
                    }
                )
                resp.status_code = 400
                return resp
            file.save(os.path.join(data_dir, filename))
            log.info(f"Data {file.filename} upload succesfull")
            resp = jsonify({
                'message': "data upload successfull"
            })
            resp.status_code = 201
        else:
            log.error(f"Unsupported data content_type, supported are {list(ALLOWED_DATA_EXTENSIONS)}")
            resp = jsonify(
                {
                    'message': f'allowed data file types are: {list(ALLOWED_DATA_EXTENSIONS)}'
                }
            )
            resp.status_code = 400
        return resp


@doc(description='Execute prediction', tags=['inference'])
class ExecuteInference(Resource, MethodResource):
    def post(self):
        from ede_handler import ede_handler
        try:
            job = queue.enqueue(ede_handler, os.path.join(conf_dir, 'ede_config_service.yaml'),
                                timout=os.getenv('RQ_TIMEOUT', 600))
            resp = jsonify({
                'job_id': job.get_id()
            })
            resp.status_code = 201
        except Exception as e:
            log.error(f"Failed to enqueue job with {type(e)} and {e.args}")
            resp = jsonify({
                'message': f"Failed to enqueue job with {type(e)} and {e.args}"
            })
            resp.status_code = 500
        return resp


# ############## RQ Workers #################
@doc(description='RQ worker status', tags=['engine'])
class RQWorkers(Resource, MethodResource):
    def get(self):
        list_workers = get_list_workers()
        worker_list = []
        for l in list_workers:
            worker = {}
            pid = get_pid_from_file(l)
            worker['id'] = l.split('/')[-1].split('.')[0].split('_')[-1]
            worker['pid'] = int(pid)
            worker['status'] = check_pid(pid)
            worker_list.append(worker)
        return jsonify({'workers': worker_list})

    def post(self):
        list_workers = get_list_workers()
        logic_cpu = psutil.cpu_count(logical=True)
        worker_threshold = os.getenv('WORKER_THRESHOLD', 2)
        if len(list_workers) > (logic_cpu - 1)*worker_threshold:
            resp = jsonify({'warning': 'maximum number of workers active!',
                                'workers': logic_cpu,
                           'threshold': worker_threshold})
            log.warning('Maximum number of aug workers reached: {}'.format(logic_cpu))
            resp.status_code = 200
            return resp
        if os.getcwd().split('/')[-1] != 'service': # TODO fix this
            p = subprocess.Popen(['python', 'service/ede_rq_worker.py'])
        else:
            p = subprocess.Popen(['python', 'ede_rq_worker.py'])
        # p = subprocess.Popen(['python', 'ede_rq_worker.py'])
        sb_pid = p.pid
        log.info("Starting EDE RQ worker {}".format(len(list_workers)))
        if check_pid(sb_pid):
            try:
                queue.get_job_ids()
            except Exception as inst:
                log.error(f'Error connecting to redis with {type(inst)} and {inst.args}')
                resp = jsonify({
                    'error': f'Error connecting to redis with {type(inst)} and {inst.args}'
                })
                resp.status_code = 500
                return resp
            resp = jsonify({'status': 'worker started',
                            'pid': sb_pid})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify({'error': 'worker failed to start'})
            resp.status_code = 500
            return resp

    def delete(self):
        list_workers = get_list_workers()
        pid_dict = {}
        failed_lst = []
        for worker in list_workers:
            pid = get_pid_from_file(worker)
            pid_dict[worker.split('/')[-1].split('.')[0]] = pid
            # kill pid
            try:
                kill_pid(pid)
            except Exception as inst:
                log.error(f"Failed to stop pid {pid} with {inst}, deleting file")
                delete_pid_file(worker)
            # check if pid is killed
            if not check_pid(pid):
                log.error(f"Failed to stop rq workers with pid {pid}")
                failed_lst.append(pid)
            # cleanup pid files
            log.info(f"Cleaning up pid file for worker {worker}")
            clean_up_pid(worker)
        if failed_lst:
            resp = jsonify({
                'message': f'failed to stop rq workers',
                'worker_pids': failed_lst
            })
            resp.status_code = 500
            return resp
        resp = jsonify({
            'message': 'all rq workers stopped',
            'workers': pid_dict
        })
        resp.status_code = 200
        return resp


@doc(description='EDE Service Jobs', tags=['engine'])
class RQEngineJobQueueStatus(Resource, MethodResource):
    def get(self):
        try:
            jobs = queue.get_job_ids()
        except Exception as inst:
            log.error(f'Error connecting to redis with {type(inst)} and {inst.args}')
            resp = jsonify({
                'error': f'Error connecting to redis with {type(inst)} and {inst.args}'
            })
            resp.status_code = 500
            return resp
        failed = queue.failed_job_registry.get_job_ids()
        jqueued = []
        started = queue.started_job_registry.get_job_ids()
        finished = queue.finished_job_registry.get_job_ids()
        for rjob in jobs:
            try:
                job = Job.fetch(rjob, connection=r_connection)
            except:
                log.error("No job with id {}".format(rjob))
                response = {'error': 'no such job'}
                return response
            if job.is_finished:
                finished.append(rjob)
            elif job.is_failed:
                failed.append(rjob)
            elif job.is_started:
                started.append(rjob)
            elif job.is_queued:
                jqueued.append(rjob)
        # check for detached EDE processes
        detached_failed = check_for_detached_process(failed)
        detached_finished = check_for_detached_process(finished)
        resp_dict = {
            'started': started,
            'finished': finished,
            'failed': failed,
            'queued': jqueued
        }
        if detached_failed:
            resp_dict['detached_failed'] = detached_failed
        if detached_finished:
            resp_dict['detached_finished'] = detached_finished
        resp = jsonify(resp_dict)
        resp.status_code = 200
        return resp

    def delete(self):
        try:
            jobs = queue.get_job_ids()
        except Exception as inst:
            log.error(f'Error connecting to redis with {type(inst)} and {inst.args}')
            resp = jsonify({
                'error': f'Error connecting to redis with {type(inst)} and {inst.args}'
            })
            resp.status_code = 500
            return resp
        for rjob in jobs:
            try:
                job = Job.fetch(rjob, connection=r_connection)
            except:
                log.error("No job with id {}".format(rjob))
                response = {'error': 'no such job'}
                return response
            job.delete()

        failed_registry = queue.failed_job_registry
        started_registry = queue.started_job_registry

        for rjob in failed_registry.get_job_ids():
            failed_registry.remove(rjob, delete_job=True)

        for rjob in started_registry.get_job_ids():
            send_stop_job_command(r_connection, rjob)
            cancel_job(rjob, connection=r_connection)
            started_registry.remove(rjob, delete_job=True)

        # kill all EDE processes
        check_for_detached_process(jobs)

        resp = jsonify(
            {
                'message': 'All jobs deleted',
                'jobs': jobs
            }
        )
        resp.status_code = 200
        return resp


@doc(description='EDE Service Job details', tags=['engine'])
class RQEngineJobStatus(Resource, MethodResource):
    def get(self, job_id):
        try:
            job = Job.fetch(job_id, connection=r_connection)
        except Exception as inst:
            log.error("No job with id {}".format(job_id))
            response = jsonify({'error': 'no job',
                                'job_id': job_id})
            response.status_code = 404
            return response
        job.refresh()
        status = job.get_status()
        finished = job.is_finished
        meta = job.meta
        response = jsonify({'status': status,
                            'finished': finished,
                            'meta': meta})
        response.status_code = 200
        return response
    def delete(self, job_id):
        try:
            job = Job.fetch(job_id, connection=r_connection)
        except Exception as inst:
            log.error("No job with id {}".format(job_id))
            response = jsonify({'error': 'no job',
                                'job_id': job_id})
            response.status_code = 404
            return response
        send_stop_job_command(r_connection, job_id)
        job.delete()
        # kill detached EDE process
        check_for_detached_process([job_id])

        response = jsonify({'status': 'deleted',
                            'job_id': job_id})
        response.status_code = 200
        return response


@doc(description="Execution platform readiness support", tags=['readiness', 'liveness'])
class ReadinessProbing(Resource, MethodResource):
    def get(self):
        response = jsonify({'ok': True, 'message': 'I am alive'})
        response.status_code = 200
        return response


# Rest API routing
api.add_resource(EDEStatus, '/', '/v1/status')
api.add_resource(Config, '/v1/config')
api.add_resource(ConnectorConfig, '/v1/config/connector')
api.add_resource(FilterConfig, '/v1/config/filter')
api.add_resource(AugmentationConfig, '/v1/config/augmentation')
api.add_resource(InferenceConfig, '/v1/config/inference')

api.add_resource(RQWorkers, '/v1/service/worker')
api.add_resource(RQEngineJobQueueStatus, '/v1/service/jobs')
api.add_resource(RQEngineJobStatus, '/v1/service/jobs/<string:job_id>')

api.add_resource(EDELogs, '/v1/logs')
api.add_resource(LocalData, '/v1/data')
api.add_resource(LocalDataHandler, '/v1/data/<string:data_file>')

api.add_resource(ExecuteInference, '/v1/detect')

api.add_resource(ReadinessProbing, '/ping')

# Rest API docs, Swagger
docs.register(EDEStatus)
docs.register(Config)
docs.register(ConnectorConfig)
docs.register(FilterConfig)
docs.register(AugmentationConfig)
docs.register(InferenceConfig)
docs.register(LocalData)
docs.register(LocalDataHandler)
docs.register(RQWorkers)
docs.register(RQEngineJobQueueStatus)
docs.register(RQEngineJobStatus)
docs.register(EDELogs)
docs.register(ExecuteInference)
docs.register(ReadinessProbing)