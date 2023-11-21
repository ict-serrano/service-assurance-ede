"""
Copyright 2021, Institute e-Austria, Timisoara, Romania
    http://www.ieat.ro/
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

import sys, getopt
import os.path
from addict import Dict
from edeconfig import readConf
from edelogger import logger
from datetime import datetime
from edengine import edengine
from util import getModelList, check_dask_settings, log_format
import time
from dask.distributed import Client, LocalCluster
from signal import signal, SIGINT
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


def main(argv,
         cluster,
         client):
    dataDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    modelsDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
    queryDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'queries')

    settings = Dict()
    settings.esendpoint = None
    settings.prendpoint = None
    settings.cthendpoint = None # Serrano
    settings.cthclusterid = None # Serrano
    settings.cthstart = None # Serrano
    settings.cthend = None # Serrano
    settings.groups = ['general'] # Serrano
    settings.etaendpoint = None # Serrano
    settings.pmdsendpoint = None # Serrano
    settings.pmdsstart = '-2h'  # Serrano
    settings.pmdsend = ''  # Serrano
    settings.pmdsgroups = ['general']  # Serrano
    settings.pmdsclusterid = None  # Serrano
    settings.pmdsnamespace = None # Serrano
    settings.influxdbendpoint = None
    settings.influxdbport = 8086
    settings.influxdbtoken = None
    settings.influxdborg = 'serrano'
    settings.influxdbbucket = 'serrano'
    settings.influxdbquery = None
    settings.Dask.SchedulerEndpoint = None  # "local"
    settings.Dask.SchedulerPort = 8787
    settings.Dask.EnforceCheck = False
    settings.prkafkaendpoint = None
    settings.prkafkaport = 9092
    settings.prkafkatopic = "edetopic"
    settings.grafanaurl = None
    settings.augmentation = None  # augmentation including scaler and user defined methods
    settings.detectionscaler = None
    settings.MPort = 9090
    settings.EDEPort = 5001
    settings.index = "logstash-*"
    settings["from"] = None
    settings.to = None
    settings.query = None
    settings.nodes = None
    settings.qsize = None
    settings.qinterval = None
    settings.fillna = None
    settings.dropna = None
    settings.filterwild = None
    settings.filterlow = None
    settings.local = None
    settings.train = None
    settings.hpomethod = None
    settings.tpot = None
    settings.ParamDistribution = None
    settings.detecttype = None # TODO
    settings.traintype = None
    settings.validationtype = None # Todo
    settings.target = None
    settings.load = None
    settings.file = None
    settings.method = None
    settings.detectMethod = None
    settings.trainMethod = None
    settings.cv = None
    settings.trainscore = None
    settings.scorer = None
    settings.verbosecv = None
    settings.LearningCurve = None
    settings.ValidationCurve = None
    settings.PrecisionRecallCurve = None
    settings.ROCAUC = None
    settings.RFE = None
    settings.DecisionBoundary = None
    settings.PredAnalysis = None
    settings.returnestimators = None
    settings.analysis = None
    settings.validate = None
    settings.export = None
    settings.trainexport = None
    settings.detect = None  # Bool default None
    settings.cfilter = None
    settings.rfilter = None
    settings.dfilter = None
    settings.sload = None
    settings.smemory = None
    settings.snetwork = None
    settings.heap = None
    settings.checkpoint = None
    settings.delay = None
    settings.interval = None
    settings.resetindex = None
    settings.training = None
    settings.validation = None
    settings.validratio = 0.2
    settings.compare = False
    settings.anomalyOnly = False
    settings.categorical = None
    settings.point = False

    # Only for testing
    settings['validate'] = False
    dask_backend = False

    try:
        opts, args = getopt.getopt(argv, "he:tf:m:vx:d:lq:", ["endpoint=", "file=", "method=", "export=", "detect=", "query="])  # todo:expand command line options
    except getopt.GetoptError:
        logger.warning('[%s] : [WARN] Invalid argument received exiting', datetime.fromtimestamp(time.time()).strftime(log_format))
        print("ede.py -f <filelocation>, -t -m <method> -v -x <modelname>")
        sys.exit(0)
    for opt, arg in opts:
        if opt == '-h':
            print("#" * 100)
            print("H2020 ASPIDE")
            print('Event Detection Engine')
            print("-" * 100)
            print('Utilisation:')
            print('-f -> configuration file location')
            print('-t -> activate training mode')
            print('-m -> methods')
            print('   -> allowed methods: skm, em, dbscan, sdbscan, isoforest')
            print('-x -> export model name')
            print('-v -> validation')
            print('-q -> query string for anomaly/event detection')
            print("#" * 100)
            sys.exit(0)
        elif opt in ("-e", "--endpoint"):
            settings['esendpoint'] = arg
        elif opt in ("-t"):
            settings["train"] = True
        elif opt in ("-f", "--file"):
            settings["file"] = arg
        elif opt in ("-m", "--method"):
            settings["method"] = arg
        elif opt in ("-v"):
            settings["validate"] = True
        elif opt in ("-x", "--export"):
            settings["export"] = arg
        elif opt in ("-d", "--detect"):
            settings["detect"] = arg
        elif opt in ("-l", "--list-models"):
            print ("Current saved models are:\n")
            print((getModelList()))
            sys.exit(0)
        elif opt in ("-q", "--query"):
            settings["query"] = arg

    # print("#" * 100)
    # print(queryDir)
    logger.info('[{}] : [INFO] Starting EDE framework ...'.format(
        datetime.fromtimestamp(time.time()).strftime(log_format)))
    logger.info('[{}] : [INFO] Trying to read configuration file ...'.format(
        datetime.fromtimestamp(time.time()).strftime(log_format)))

    if settings["file"] is None:
        file_conf = 'ede_config.yaml'
        logger.info('[%s] : [INFO] Settings file set to %s',
                            datetime.fromtimestamp(time.time()).strftime(log_format), file_conf)
    else:
        if os.path.isfile(settings["file"]):
            file_conf = settings["file"]
            logger.info('[%s] : [INFO] Settings file set to %s',
                        datetime.fromtimestamp(time.time()).strftime(log_format), file_conf)
        else:
            logger.error('[%s] : [ERROR] Settings file not found at locations %s',
                        datetime.fromtimestamp(time.time()).strftime(log_format), settings["file"])
            sys.exit(1)

    readCnf = readConf(file_conf)
    logger.info('[{}] : [INFO] Reading configuration file ...'.format(
        datetime.fromtimestamp(time.time()).strftime(log_format)))

    # TODO: create def dls(file_conf)
    # Connector
    try:
        logger.info('[{}] : [INFO] Index Name set to : {}'.format(
            datetime.fromtimestamp(time.time()).strftime(log_format),
            readCnf['Connector']['indexname']))
    except Exception:
        logger.warning('[%s] : [WARN] Index not set in conf setting to default value %s',
                            datetime.fromtimestamp(time.time()).strftime(log_format), settings['index'])
    if settings['pmdsendpoint'] is None:
        try:
            logger.info('[{}] : [INFO] PMDS set to : {}'.format(
                datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                readCnf['Connector']['PMDS']['Endpoint']))
            settings['pmdsendpoint'] = readCnf['Connector']['PMDS']['Endpoint']
            try:
                logger.info('[{}] : [INFO] PMDS CLuster ID set to : {}'.format(
                    datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                    readCnf['Connector']['PMDS']['Cluster_id']))
                settings['pmdsclusterid'] = readCnf['Connector']['PMDS']['Cluster_id']
            except:
                logger.warning('[%s] : [WARN] PMDS Cluster ID not set in conf setting to default value %s',
                               datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                               settings['pmdsclusterid'])

            try:
                logger.info('[{}] : [INFO] PMDS Start set to  {}'.format(
                    datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                    readCnf['Connector']['PMDS']['Start']))
                settings['pmdsstart'] = readCnf['Connector']['PMDS']['Start']
            except:
                logger.warning('[%s] : [WARN] PMDS Start not set in conf setting to default value %s',
                               datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                               settings['pmdsstart'])

            try:
                logger.info('[{}] : [INFO] PMDS End set to {}'.format(
                    datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                    readCnf['Connector']['PMDS']['End']))
                settings['pmdsend'] = readCnf['Connector']['PMDS']['End']
            except:
                logger.warning('[%s] : [WARN] PMDS End not set in conf setting to default value %s',
                               datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                               settings['pmdsend'])
            try:
                logger.info('[{}] : [INFO] PMDS Metrics set to '.format(
                    datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                    readCnf['Connector']['PMDS']['Metrics']))
                settings['pmdsmetrics'] = readCnf['Connector']['PMDS']['Metrics']
            except:
                pass

            try:
                logger.info('[{}] : [INFO] PMDS Groups set to {}'.format(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                    readCnf['Connector']['PMDS']['Groups']))
                settings['pmdsgroups'] = readCnf['Connector']['PMDS']['Groups']
            except:
                logger.warning('[%s] : [WARN] PMDS Groups not set in conf setting to default value %s', datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                               settings['pmdsgroups'])

            try:
                logger.info('[{}] : [INFO] PMDS Namespace set to {}'.format(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), readCnf['Connector']['PMDS']['Namespace']))
                settings['pmdsnamespace'] = readCnf['Connector']['PMDS']['Namespace']
            except:
                logger.warning('[%s] : [WARN] PMDS Namespace not set in conf setting to default value %s',
                               datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                               settings['pmdsnamespace'])

        except:
            logger.warning('[%s] : [WARN] PMDS not set in conf',
                                datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    elif settings['influxdbendpoint'] is None and settings['esendpoint'] is None and settings['prendpoint'] is None:
        try:
            logger.info('[{}] : [INFO] InfluxDB set to : {}'.format(
                datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                readCnf['Connector']['InfluxDB']['endpoint']))
            settings['influxdbendpoint'] = readCnf['Connector']['InfluxDB']['endpoint']
        except Exception:
            logger.error('[%s] : [ERROR] InfluxDB endpoint not set in conf exiting ...',
                            datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
            sys.exit(2)
        try:
            logger.info('[{}] : [INFO] InfluxDB Port set to : {}'.format(
                datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                readCnf['Connector']['InfluxDB']['port']))
            settings['influxdbport'] = readCnf['Connector']['InfluxDB']['port']
        except Exception:
            logger.warning('[%s] : [WARN] InfluxDB Port not set in conf setting to default value %s',
                           datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), settings['influxdbport'])
        try:
            settings['influxdbtoken'] = readCnf['Connector']['InfluxDB']['token']
            logger.info('[{}] : [INFO] InfluxDB Token found ..'.format(
                datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))
        except Exception:
            logger.error('[%s] : [ERROR] InfluxDB token not set in conf exiting ...',
                            datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
            sys.exit(2)
        try:
            settings['influxdborg'] = readCnf['Connector']['InfluxDB']['org']
            logger.info('[{}] : [INFO] InfluxDB Org set to {}}'.format(
                datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), settings['influxdborg']))
        except Exception:
            logger.warning('[%s] : [WARN] InfluxDB Org not set in conf setting to default value %s',
                           datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), settings['influxdborg'])
        try:
            settings['influxdbbucket'] = readCnf['Connector']['InfluxDB']['bucket']
            logger.info('[{}] : [INFO] InfluxDB Bucket set to {}'.format(
                datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), settings['influxdbbucket']))
        except Exception:
            logger.warning('[%s] : [WARN] InfluxDB Bucket not set in conf setting to default value %s',
                           datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), settings['influxdbbucket'])
        try:
            settings['influxdbquery'] = readCnf['Connector']['InfluxDB']['query']
            logger.info('[{}] : [INFO] InfluxDB Flux Query set ...'.format(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), settings['influxdbquery']))
        except Exception:
            logger.error('[%s] : [ERROR] InfluxDB Flux Query not set in conf exiting ...', datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
            sys.exit(2)
    elif settings['esendpoint'] is None:
        try:
            logger.info('[{}] : [INFO] Monitoring ES Backend endpoint in config {}'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format),
                readCnf['Connector']['ESEndpoint']))
            settings['esendpoint'] = readCnf['Connector']['ESEndpoint']
        except Exception:

            try:
                settings['prendpoint'] = readCnf['Connector']['PREndpoint']
                logger.info('[{}] : [INFO] Monitoring PR Endpoint set to {}'.format(
                    datetime.fromtimestamp(time.time()).strftime(log_format),
                    settings["prendpoint"]))
            except Exception:
                settings['prendpoint'] = None

            # if readCnf['Connector']['PREndpoint'] is None:  # todo; now only available in config file not in commandline
            #     logger.error('[%s] : [ERROR] ES and PR backend Enpoints not set in conf or commandline!',
            #                     datetime.fromtimestamp(time.time()).strftime(log_format))
            #     sys.exit(1)
            # else:
            #     settings['prendpoint'] = readCnf['Connector']['PREndpoint']
            #     logger.info('[{}] : [INFO] Monitoring PR Endpoint set to {}'.format(datetime.fromtimestamp(time.time()).strftime(log_format),
            #                 settings["prendpoint"]))
    else:
        logger.info('[%s] : [INFO] ES Backend Enpoint set to %s',
                            datetime.fromtimestamp(time.time()).strftime(log_format), settings['esendpoint'])
    if settings['pmdsendpoint']:
        pass
    else:
        if settings["from"] is None:
            try:
                settings["from"] = readCnf['Connector']['From']
                logger.info('[%s] : [INFO] From timestamp set to %s',
                            datetime.fromtimestamp(time.time()).strftime(log_format),
                            settings["from"])
            except Exception:
                # logger.info('[{}] : [INFO] PR Backend endpoint set to {}'.format(
                #     datetime.fromtimestamp(time.time()).strftime(log_format), settings['prendpoint']))
                if settings['prendpoint'] is not None:
                    pass
                    # logger.info('[{}] : [INFO] PR Backend endpoint set to {}'.format(datetime.fromtimestamp(time.time()).strftime(log_format), settings['prendpoint']))
                else:
                    try:
                        readCnf['Connector']['Local']  # todo check if local exists in conf (elegant solution is needed)
                    except Exception:
                        logger.error('[%s] : [ERROR] From timestamp not set in conf or commandline!',
                                 datetime.fromtimestamp(time.time()).strftime(log_format))
                        sys.exit(1)
        else:
            logger.info('[%s] : [INFO] From timestamp set to %s',
                        datetime.fromtimestamp(time.time()).strftime(log_format), settings['from'])

        if settings["to"] is None:
            try:
                settings["to"] = readCnf['Connector']['to']
                logger.info('[%s] : [INFO] To timestamp set to %s',
                                    datetime.fromtimestamp(time.time()).strftime(log_format),
                                    settings["to"])
            except Exception:
                if settings['prendpoint'] is not None:
                    pass
                else:
                    try:
                        readCnf['Connector']['Local']  # todo check if local exists in conf (elegant solution is needed)
                    except Exception:
                        logger.error('[%s] : [ERROR] To timestamp not set in conf or commandline!',
                                             datetime.fromtimestamp(time.time()).strftime(log_format))
                        sys.exit(1)
        else:
            logger.info('[%s] : [INFO] To timestamp set to %s',
                        datetime.fromtimestamp(time.time()).strftime(log_format), settings['to'])

        if settings['query'] is None:
            try:
                settings['query'] = readCnf['Connector']['Query']
                logger.info('[%s] : [INFO] Query set to %s',
                                    datetime.fromtimestamp(time.time()).strftime(log_format),
                                    settings['query'])
            except Exception:
                if settings['prendpoint'] is not None:
                    pass
                logger.error('[%s] : [ERROR] Query not set in conf or commandline!',
                                     datetime.fromtimestamp(time.time()).strftime(log_format))
                sys.exit(1)
        else:
            logger.info('[%s] : [INFO] Query set to %s',
                               datetime.fromtimestamp(time.time()).strftime(log_format), settings['query'])

    if settings.prkafkaendpoint is None:
        try:
            settings.prkafkaendpoint = readCnf['Connector']['KafkaEndpoint']
            if settings.prkafkaendpoint == 'None':
                settings.prkafkaendpoint = None
            else:
                settings.prkafkatopic = readCnf['Connector']['KafkaTopic']
                settings.prkafkaport = readCnf['Connector']['KafkaPort']
            logger.info('[{}] : [INFO] Kafka Endpoint set to  {}'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format), settings.prkafkaendpoint))
        except Exception:
            logger.warning('[{}] : [WARN] Kafka Endpoint not set.'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format), settings.prkafkaendpoint))
    # Grafana settings
    if settings.grafanaurl is None:
        try:
            settings.grafanaurl = readCnf['Connector']['GrafanaUrl']
            if settings.grafanaurl == 'None':
                settings.grafanaurl = None
            else:
                settings.grafanatoken = readCnf['Connector']['GrafanaToken']
                settings.grafanatag = readCnf['Connector']['GrafanaTag']
            logger.info('[{}] : [INFO] Grafana Endpoint set to  {}'.format(
                datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), settings.grafanaurl))
        except:
            logger.warning('[{}] : [WARN] Grafana Endpoint not set.'.format(
                datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))

    if settings["nodes"] is None:
        try:
            if not readCnf['Connector']['nodes']:
                readCnf['Connector']['nodes'] = 0
            settings["nodes"] = readCnf['Connector']['nodes']
            logger.info('[%s] : [INFO] Desired nodes set to %s',
                    datetime.fromtimestamp(time.time()).strftime(log_format),
                    settings['nodes'])
        except Exception:
            logger.warning('[%s] : [WARN] No nodes selected from config file or comandline querying all',
                           datetime.fromtimestamp(time.time()).strftime(log_format))
            settings["nodes"] = 0
    else:
        logger.info('[%s] : [INFO] Desired nodes set to %s',
                    datetime.fromtimestamp(time.time()).strftime(log_format), settings["nodes"])

    if settings["qsize"] is None:
        try:
            settings["qsize"] = readCnf['Connector']['QSize']
            logger.info('[%s] : [INFO] Query size set to %s',
                                datetime.fromtimestamp(time.time()).strftime(log_format),
                                settings['qsize'])
        except Exception:
            logger.warning('[%s] : [WARN] Query size not set in conf or commandline setting to default',
                                 datetime.fromtimestamp(time.time()).strftime(log_format))
            settings["qsize"] = 'default'
    else:
        logger.info('[%s] : [INFO] Query size set to %s',
                    datetime.fromtimestamp(time.time()).strftime(log_format), settings["qsize"])

    if settings["qinterval"] is None:
        try:
            settings["qinterval"] = readCnf['Connector']['MetricsInterval']
            logger.info('[%s] : [INFO] Metric Interval set to %s',
                                datetime.fromtimestamp(time.time()).strftime(log_format),
                                settings['qinterval'])
        except Exception:
            logger.warning('[%s] : [WARN] Metric Interval not set in conf or commandline setting to default',
                                 datetime.fromtimestamp(time.time()).strftime(log_format))
            settings["qsize"] = "default"
    else:
        logger.info('[%s] : [INFO] Metric interval set to %s',
                    datetime.fromtimestamp(time.time()).strftime(log_format), settings["qinterval"])
    if readCnf['Connector']['Dask']:
        try:
            settings['Dask']['SchedulerEndpoint'] = readCnf['Connector']['Dask']['SchedulerEndpoint']
            settings['Dask']['SchedulerPort'] = readCnf['Connector']['Dask']['SchedulerPort']
            settings['Dask']['EnforceCheck'] = readCnf['Connector']['Dask']['EnforceCheck']
            logger.info('[{}] : [INFO] Dask scheduler  set to: endpoint {}, port {}, check {}'.format(
        datetime.fromtimestamp(time.time()).strftime(log_format), settings['Dask']['SchedulerEndpoint'],
                settings['Dask']['SchedulerPort'], settings['Dask']['EnforceCheck']))
            dask_backend = True
        except Exception:
            logger.warning('[{}] : [WARN] Dask scheduler  set to default values'.format(datetime.fromtimestamp(time.time()).strftime(log_format)))
            dask_backend = False

    if settings['local'] is None:
        try:
            settings['local'] = readCnf['Connector']['Local']
            logger.info('[{}] : [INFO] Local datasource set to {}'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format), settings['local']))
        except Exception:
            logger.info('[{}] : [INFO] Local datasource set to default'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format)))
            settings['local'] = None
            if settings['esendpoint'] is None and settings['prendpoint'] is None and settings['pmdsendpoint'] is None:
                logger.error('[{}] : [ERROR] No valid datasource set! Exiting ...'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format)))
                sys.exit(1)
    else:
        logger.info('[{}] : [INFO] Local datasource set to {}'.format(
            datetime.fromtimestamp(time.time()).strftime(log_format), settings['local']))
    # Mode
    if settings["train"] is None:
        try:
            settings["train"] = readCnf['Mode']['Training']
            logger.info('[%s] : [INFO] Train is set to %s from conf',
                            datetime.fromtimestamp(time.time()).strftime(log_format), settings['train'])
        except Exception:
            logger.error('[%s] : [ERROR] Train is not set in conf or comandline!',
                            datetime.fromtimestamp(time.time()).strftime(log_format))
            sys.exit(1)
    else:
        logger.info('[%s] : [INFO] Train is set to %s from comandline',
                            datetime.fromtimestamp(time.time()).strftime(log_format), settings['train'])

    # Analysis
    if settings.analysis is None:
        try:
            logger.info('[{}] : [INFO] Loading user defined analysis'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format)))
            settings.analysis = readCnf['Analysis']
        except Exception:
            logger.info('[{}] : [INFO] No user defined analysis detected'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format)))

    # Validate
    if settings["validate"] is None:
        try:
            settings["validate"] = readCnf['Mode']['Validate']
            logger.info('[%s] : [INFO] Validate is set to %s from conf',
                            datetime.fromtimestamp(time.time()).strftime(log_format), settings['validate'])
        except Exception:
            logger.error('[%s] : [ERROR] Validate is not set in conf or comandline!',
                                 datetime.fromtimestamp(time.time()).strftime(log_format))
            sys.exit(1)
    else:
        logger.info('[%s] : [INFO] Validate is set to %s from comandline',
                            datetime.fromtimestamp(time.time()).strftime(log_format), settings['validate'])

    # Detect
    if settings["detect"] is None:
        try:
            settings["detect"] = readCnf['Mode']['Detect']
            logger.info('[%s] : [INFO] Detect is set to %s from conf',
                            datetime.fromtimestamp(time.time()).strftime(log_format), settings['detect'])
        except Exception:
            logger.error('[%s] : [ERROR] Detect is not set in conf or comandline!',
                                 datetime.fromtimestamp(time.time()).strftime(log_format))
            sys.exit(1)
    else:
        logger.info('[%s] : [INFO] Detect is set to %s from comandline',
                            datetime.fromtimestamp(time.time()).strftime(log_format), settings['detect'])

    if settings["detectMethod"] is None:
        try:
            settings["detectMethod"] = readCnf['Detect']['Method']
            logger.info('[%s] : [INFO] Detect Method is set to %s from conf',
                            datetime.fromtimestamp(time.time()).strftime(log_format), settings["detectMethod"])
        except Exception:
            logger.error('[%s] : [ERROR] Detect Method is not set in conf or comandline!',
                                 datetime.fromtimestamp(time.time()).strftime(log_format))
            sys.exit(1)
    else:
        logger.info('[%s] : [INFO] Detect Method is set to %s from comandline',
                            datetime.fromtimestamp(time.time()).strftime(log_format), settings["detectMethod"])

    if settings["detecttype"] is None:
        try:
            settings["detecttype"] = readCnf['Detect']['Type']
            logger.info('[{}] : [INFO] Detect Type is set to {} from conf'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format), settings["detecttype"]))
        except Exception:
            logger.error('[%s] : [ERROR] Detect Type is not set in conf or command line!',
                                 datetime.fromtimestamp(time.time()).strftime(log_format))
            sys.exit(1)
    else:
        logger.info('[%s] : [INFO] Detect Type is set to %s from command line',
                            datetime.fromtimestamp(time.time()).strftime(log_format), settings["detecttype"])

    if settings['PredAnalysis'] is None:
        try:
            settings['PredAnalysis'] = readCnf['Detect']['Analysis']
            logger.info('[{}] : [INFO] Detect Analysis is set to {} from conf'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format), settings["PredAnalysis"]))
        except Exception:
            settings['PredAnalysis'] = False

    if settings["trainMethod"] is None:
        try:
            settings["trainMethod"] = readCnf['Training']['Method']
            logger.info('[%s] : [INFO] Train Method is set to %s from conf',
                            datetime.fromtimestamp(time.time()).strftime(log_format), settings["trainMethod"])
        except Exception:
            try:
                settings['Training']['TPOTParam']
            except Exception:
                logger.error('[%s] : [ERROR] Train Method is not set in conf or comandline!',
                                     datetime.fromtimestamp(time.time()).strftime(log_format))
                sys.exit(1)
    else:
        logger.info('[%s] : [INFO] Train Method is set to %s from comandline',
                            datetime.fromtimestamp(time.time()).strftime(log_format), settings["trainMethod"])

    if settings["traintype"] is None:
        try:
            settings["traintype"] = readCnf['Training']['Type']
            logger.info('[%s] : [INFO] Train Type is set to %s from conf',
                        datetime.fromtimestamp(time.time()).strftime(log_format), settings["traintype"])
        except Exception:
            logger.error('[%s] : [ERROR] Train Type is not set in conf or command line!',
                         datetime.fromtimestamp(time.time()).strftime(log_format))
            sys.exit(1)
    else:
        logger.info('[%s] : [INFO] Train Type is set to %s from command line',
                    datetime.fromtimestamp(time.time()).strftime(log_format), settings["traintype"])
    if settings.target is None:
        try:
            settings.target = readCnf['Training']['Target']
            logger.info('[{}] : [INFO] Classification Target set to {}'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format), settings.target))
        except Exception:
            if settings['traintype'] == 'classification':
                logger.warning('[{}] : [WARN] Classification Target not set in config'.format(
                    datetime.fromtimestamp(time.time()).strftime(log_format), settings.target))
            else:
                pass

    if settings.hpomethod is None:
        try:
            settings.hpomethod = readCnf['Training']['HPOMethod']
            logger.info('[{}] : [INFO] HPO method set to {}'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format), settings.hpomethod))
            try:
                settings.hpoparam = readCnf['Training']['HPOParam']
                for k, v in readCnf['Training']['HPOParam'].items():
                    logger.info('[{}] : [INFO] HPO Method {}  Param {} set to {}'.format(
                        datetime.fromtimestamp(time.time()).strftime(log_format), settings.hpomethod, k, v))
            except Exception:
                logger.warn('[{}] : [WARN] HPO Method Params set to default!'.format(
                    datetime.fromtimestamp(time.time()).strftime(log_format)))
                settings.hpoparam = {}
        except Exception:
            if readCnf['Training']['Type'] == 'hpo':
                logger.error('[{}] : [ERROR] HPO invoked without method! Exiting'.format(
                    datetime.fromtimestamp(time.time()).strftime(log_format), settings.hpomethod))
                sys.exit(1)
            else:
                pass

    if settings.ParamDistribution is None:
        try:
            settings.ParamDistribution = readCnf['Training']['ParamDistribution']
            logger.info('[{}] : [INFO] HPO Parameter Distribution found.'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format)))
        except Exception:
            if readCnf['Training']['Type'] == 'hpo':
                logger.error('[{}] : [ERROR] HPO invoked without Parameter distribution! Exiting'.format(
                    datetime.fromtimestamp(time.time()).strftime(log_format), settings.hpomethod))
                sys.exit(1)
            else:
                pass
    if settings.tpot is None:
        try:
            settings.tpot = readCnf['Training']['TPOTParam']
            logger.info('[{}] : [INFO] TPO Parameters  found.'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format)))
        except Exception:
            try:
                if readCnf['Training']['Type'] == 'tpot':
                    settings.tpot = {}
                    logger.warning('[{}] : [WARN] TPO Parameters not found. Using defaults'.format(
                        datetime.fromtimestamp(time.time()).strftime(log_format)))
                else:
                    pass
            except Exception:
                pass

    if settings["export"] is None:
        try:
            settings["export"] = readCnf['Training']['Export']
            logger.info('[%s] : [INFO] Export is set to %s from conf',
                            datetime.fromtimestamp(time.time()).strftime(log_format), settings["export"])
        except Exception:
            logger.error('[%s] : [ERROR] Export is not set in conf or comandline!',
                                 datetime.fromtimestamp(time.time()).strftime(log_format))
            sys.exit(1)
    else:
        logger.info('[%s] : [INFO] Model is set to %s from comandline',
                            datetime.fromtimestamp(time.time()).strftime(log_format), settings["export"])

    if settings.cv is None:
        try:
            settings.cv = readCnf['Training']['CV']
            try:
                logger.info('[{}] : [INFO] Cross Validation set to {}'.format(
                    datetime.fromtimestamp(time.time()).strftime(log_format), settings['cv']['Type']))
            except Exception:
                logger.info('[{}] : [INFO] Cross Validation set to {}'.format(
                    datetime.fromtimestamp(time.time()).strftime(log_format), settings['cv']))
                try:
                    settings['cv'] = int(settings['cv'])
                except Exception:
                    logger.error('[{}] : [ERROR] Issues with CV definition in Training!'.format(
                        datetime.fromtimestamp(time.time()).strftime(log_format)))
                    sys.exit(1)
        except Exception:
            logger.info('[{}] : [INFO] Cross Validation not defined'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format)))

    if settings.trainscore is None:
        try:
            settings.trainscore = readCnf['Training']['TrainScore']
            logger.info('[{}] : [INFO] Cross Validation set to include training scores'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format)))
        except Exception:
            settings.trainscore = False

    if settings.scorer is None:
        try:
            settings.scorer = readCnf['Training']['Scorers']
            logger.info('[{}] : [INFO] Training scorers defined'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format)))
        except Exception:
            logger.info('[{}] : [INFO] No Training scorers defined'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format)))

    if settings.verbosecv is None:
        try:
            settings.verbosecv = readCnf['Training']['Verbose']
            logger.info('[{}] : [INFO] Training verbose CV set'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format)))
        except Exception:
            pass

    if settings.LearningCurve is None:
        try:
            settings.LearningCurve = readCnf['Training']['LearningCurve']
            logger.info('[{}] : [INFO] Training Learning Curve set'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format)))
        except Exception:
            pass

    if settings.ValidationCurve is None:
        try:
            settings.ValidationCurve = readCnf['Training']['ValidationCurve']
            logger.info('[{}] : [INFO] Training Validation Curve set'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format)))
        except Exception:
            pass

    if settings.PrecisionRecallCurve is None:
        try:
            settings.PrecisionRecallCurve = readCnf['Training']['PrecisionRecallCurve']
            logger.info('[{}] : [INFO] Training Precision Recall Curve set'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format)))
        except Exception:
            pass

    if settings.ROCAUC is None:
        try:
            settings.ROCAUC = readCnf['Training']['ROCAUC']
            logger.info('[{}] : [INFO] Training ROC-AUC Curve set'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format)))
        except Exception:
            pass

    if settings.RFE is None:
        try:
            settings.RFE = readCnf['Training']['RFE']
            logger.info('[{}] : [INFO] Training Recursive Feature Elimination set'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format)))
        except Exception:
            pass

    if settings.DecisionBoundary is None:
        try:
            settings.DecisionBoundary = readCnf['Training']['DecisionBoundary']
            logger.info('[{}] : [INFO] Training Decision Boundary set'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format)))
        except Exception:
            pass

    if settings.returnestimators is None:
        try:
            settings.returnestimators = readCnf['Training']['ReturnEstimators']
            logger.info('[{}] : [INFO] CV Estimators will be saved'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format)))
        except Exception:
            settings.returnestimators = False

    if settings["load"] is None:
        try:
            settings["load"] = readCnf['Detect']['Load']
            logger.info('[%s] : [INFO] Load is set to %s from conf',
                            datetime.fromtimestamp(time.time()).strftime(log_format), settings["load"])
        except Exception:
            logger.error('[%s] : [ERROR] Load is not set in conf or comandline!',
                                 datetime.fromtimestamp(time.time()).strftime(log_format))
            sys.exit(1)
    else:
        logger.info('[%s] : [INFO] Load is set to %s from comandline',
                            datetime.fromtimestamp(time.time()).strftime(log_format), settings["load"])

    if settings.detectionscaler is None:
        try:
            settings.detectionscaler = readCnf['Detect']['Scaler']
            logger.info('[{}] : [INFO] Detection Scaler set to {}'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format), settings.detectionscaler))
        except Exception:
            settings.detectionscaler = None
            logger.warning('[{}] : [WARN] Detection scaler not specified'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format)))

    try:
        settings['MethodSettings'] = {}   #todo read settings from commandline ?
        for name, value in readCnf['Training']['MethodSettings'].items():
            # print("%s -> %s" % (name, value))
            settings['MethodSettings'][name] = value
    except Exception:
        settings['MethodSettings'] = None
        logger.warning('[%s] : [WARN] No Method settings detected, using defaults for %s!',
                            datetime.fromtimestamp(time.time()).strftime(log_format), settings["method"])

    # Augmentation
    try:
        settings['augmentation'] = readCnf['Augmentation']
        logger.info('[%s] : [INFO] Augmentations loaded',
                    datetime.fromtimestamp(time.time()).strftime(log_format))
    except Exception:
        settings['augmentation'] = None
        logger.info('[%s] : [INFO] Augmentations not defined',
                    datetime.fromtimestamp(time.time()).strftime(log_format))

    # Point anomaly settings
    try:
        settings["smemory"] = readCnf['Point']['memory']
        logger.info('[%s] : [INFO] System memory is set to %s',
                datetime.fromtimestamp(time.time()).strftime(log_format), settings["smemory"])
    except Exception:
        settings["smemory"] = "default"
        logger.warning('[%s] : [WARN] System memory is not set, using default!',
                    datetime.fromtimestamp(time.time()).strftime(log_format))

    try:
        settings["sload"] = readCnf['Point']['load']
        logger.info('[%s] : [INFO] System load is  set to %s',
                    datetime.fromtimestamp(time.time()).strftime(log_format), settings["sload"])
    except Exception:
        settings["sload"] = "default"
        logger.warning('[%s] : [WARN] System load is not set, using default!',
                    datetime.fromtimestamp(time.time()).strftime(log_format))

    try:
        settings["snetwork"] = readCnf['Point']['network']
        logger.info('[%s] : [INFO] System netowrk is  set to %s',
                    datetime.fromtimestamp(time.time()).strftime(log_format), settings["snetwork"])
    except Exception:
        settings["snetwork"] = "default"
        logger.warning('[%s] : [WARN] System network is not set, using default!',
                    datetime.fromtimestamp(time.time()).strftime(log_format))

    try:
        settings['heap'] = readCnf['Misc']['heap']
        logger.info('[%s] : [INFO] Heap size set to %s',
                datetime.fromtimestamp(time.time()).strftime(log_format), settings['heap'])
    except Exception:
        settings['heap'] = '512m'
        logger.info('[%s] : [INFO] Heap size set to default %s',
                datetime.fromtimestamp(time.time()).strftime(log_format), settings['heap'])

    # Filter
    try:
        if readCnf['Filter']['Columns']:
            logger.info('[{}] : [INFO] Filter columns set in config as {}.'.format(
        datetime.fromtimestamp(time.time()).strftime(log_format), readCnf['Filter']['Columns']))
            settings["cfilter"] = readCnf['Filter']['columns']
        else:
            logger.info('[{}] : [INFO] Filter columns set in config as {}.'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format), settings["cfilter"]))
    except Exception:
        pass
    finally:
        logger.info('[%s] : [INFO] Filter column set to %s',
                datetime.fromtimestamp(time.time()).strftime(log_format), settings['cfilter'])

    try:
        # logger.info('[%s] : [INFO] Filter rows set to %s',
        #             datetime.fromtimestamp(time.time()).strftime(log_format), readCnf['Filter']['Rows'])
        settings["rfilter"] = readCnf['Filter']['Rows']
    except Exception:
        pass
        # logger.info('[%s] : [INFO] Filter rows  %s',
        #             datetime.fromtimestamp(time.time()).strftime(log_format), settings["rfilter"])
    finally:
        logger.info('[%s] : [INFO] Filter rows set to %s',
                    datetime.fromtimestamp(time.time()).strftime(log_format), settings['rfilter'])

    try:
        if readCnf['Filter']['DColumns']:
            # print("Filter drop columns -> %s" % readCnf['Filter']['DColumns'])
            settings["dfilter"] = readCnf['Filter']['DColumns']
        else:
            # print("Filter drop columns -> %s" % settings["dfilter"])
            pass
    except Exception:
        # print("Filter drop columns -> %s" % settings["dfilter"])
        pass
    finally:
        logger.info('[%s] : [INFO] Filter drop column set to %s',
                    datetime.fromtimestamp(time.time()).strftime(log_format), settings['dfilter'])

    try:
        if readCnf['Filter']['Fillna']:
            settings['fillna'] = readCnf['Filter']['Fillna']
        else:
            settings['fillna'] = False
        logger.info('[{}] : [INFO] Fill None values set to {}'.format(
            datetime.fromtimestamp(time.time()).strftime(log_format), readCnf['Filter']['Fillna']))
    except Exception:
        logger.info('[{}] : [INFO] Fill None not set, skipping ...'.format(
        datetime.fromtimestamp(time.time()).strftime(log_format)))
        settings['fillna'] = False

    try:
        if readCnf['Filter']['Dropna']:
            settings['dropna'] = readCnf['Filter']['Dropna']
        else:
            settings['dropna'] = False
        logger.info('[{}] : [INFO] Drop None values set to {}'.format(
            datetime.fromtimestamp(time.time()).strftime(log_format), readCnf['Filter']['Dropna']))
    except Exception:
        logger.info('[{}] : [INFO] Drop None not set, skipping ...'.format(
            datetime.fromtimestamp(time.time()).strftime(log_format)))
        settings['dropna'] = False

    try:
        if readCnf['Filter']['LowVariance']:
            settings['filterlow'] = readCnf['Filter']['LowVariance']
        else:
            settings['filterlow'] = False
        logger.info('[{}] : [INFO] Low Variance filter set to {}'.format(
            datetime.fromtimestamp(time.time()).strftime(log_format), readCnf['Filter']['LowVariance']))
    except Exception:
        logger.info('[{}] : [INFO] Low Variance filter not set, skipping ...'.format(
            datetime.fromtimestamp(time.time()).strftime(log_format)))
        settings['filterlow'] = False

    try:
        if readCnf['Filter']['DWild']:
            settings['filterwild'] = readCnf['Filter']['DWild']
        else:
            settings['filterwild'] = False
        logger.info('[{}] : [INFO] Drop based on wildcard  set to {}'.format(
            datetime.fromtimestamp(time.time()).strftime(log_format), readCnf['Filter']['DWild']))
    except Exception:
        logger.info('[{}] : [INFO] Drop based on wildcard not set, skipping ...'.format(
            datetime.fromtimestamp(time.time()).strftime(log_format)))
        settings['filterwild'] = False

    if settings["checkpoint"] is None:
        try:

            settings["checkpoint"] = readCnf['Misc']['checkpoint']
            logger.info('[%s] : [INFO] Checkpointing is  set to %s',
                        datetime.fromtimestamp(time.time()).strftime(log_format), settings['checkpoint'])
        except Exception:
            settings["checkpoint"] = "True"
            logger.info('[%s] : [INFO] Checkpointing is  set to True',
                    datetime.fromtimestamp(time.time()).strftime(log_format))
    else:
        logger.info('[%s] : [INFO] Checkpointing is  set to %s',
                datetime.fromtimestamp(time.time()).strftime(log_format), settings['checkpoint'])

    if settings["delay"] is None:
        try:

            settings["delay"] = readCnf['Misc']['delay']
            # logger.info('[%s] : [INFO] Delay is  set to %s',
            #         datetime.fromtimestamp(time.time()).strftime(log_format), settings['delay'])
        except Exception:
            settings["delay"] = "2m"
        logger.info('[%s] : [INFO] Delay is  set to %s',
                    datetime.fromtimestamp(time.time()).strftime(log_format), settings['delay'])
    else:
        logger.info('[%s] : [INFO] Delay is  set to %s',
                datetime.fromtimestamp(time.time()).strftime(log_format), settings['delay'])

    if settings["interval"] is None:
        try:

            settings["interval"] = readCnf['Misc']['interval']
            logger.info('[%s] : [INFO] Interval is  set to %s',
                        datetime.fromtimestamp(time.time()).strftime(log_format), settings['interval'])
        except Exception:

            settings["interval"] = "15m"
            logger.info('[%s] : [INFO] Interval is  set to %s',
                        datetime.fromtimestamp(time.time()).strftime(log_format), settings['interval'])
    else:
        logger.info('[%s] : [INFO] Interval is  set to %s',
                        datetime.fromtimestamp(time.time()).strftime(log_format), settings['interval'])

    if settings["resetindex"] is None:
        try:

            settings["resetindex"] = readCnf['Misc']['resetindex']
        except Exception:

            settings["resetindex"] = False
    else:
        logger.info('[%s] : [INFO] Reset index set to %s',
                    datetime.fromtimestamp(time.time()).strftime(log_format), settings['resetindex'])

    try:
        settings['EDEPort'] = readCnf['Connector']['EDEPort']
        logger.info('[{}] : [INFO] EDEPort is set to {}'.format(
            datetime.fromtimestamp(time.time()).strftime(log_format),
            settings['EDEPort']))
    except Exception:
        logger.info('[%s] : [INFO] EDEPort is set to %s"',
                    datetime.fromtimestamp(time.time()).strftime(log_format), str(settings['EDEPort']))

    try:
        settings['training'] = readCnf['Detect']['training']
        logger.info('[{}] : [INFO] Classification Training set is {}'.format(
            datetime.fromtimestamp(time.time()).strftime(log_format),
            readCnf['Detect']['training']))
    except Exception:
        logger.info('[%s] : [INFO] Classification Training set is %s',
                    datetime.fromtimestamp(time.time()).strftime(log_format), str(settings['training']))

    # try:
    #     print("Classification Validation set is %s" % readCnf['Detect']['validation'])
    #     settings['validation'] = readCnf['Detect']['validation']
    # except Exception:
    #     print("Classification Validation set is default")
    # logger.info('[%s] : [INFO] Classification Validation set is %s',
    #             datetime.fromtimestamp(time.time()).strftime(log_format), str(settings['validation']))


    try:
        # print("Classification validation ratio is set to %d" % int(readCnf['Training']['ValidRatio']))
        logger.info('[{}] : [INFO] Classification validation ratio is set to {}'.format(
            datetime.fromtimestamp(time.time()).strftime(log_format), readCnf['Training']['ValidRatio']))
        if float(readCnf['Training']['ValidRatio']) > 1.0:
            # print("Validation ratio is out of range, must be between 1.0 and 0.1")
            settings['validratio'] = 0.0
            logger.warning('[{}] : [WARN] Validation ratio is out of range, must be between 1.0 and 0.1, overwritting'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format), readCnf['Training']['ValidRatio']))
        settings['validratio'] = float(readCnf['Detect']['validratio'])
    except Exception:
        logger.warning('[{}] : [WARN] Validation ratio is set to default'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format)))
    logger.info('[%s] : [INFO] Classification Validation ratio is %s',
                datetime.fromtimestamp(time.time()).strftime(log_format), str(settings['validratio']))

    # try:
    #     print("Classification comparison is set to %s" % readCnf['Detect']['compare'])
    #     settings['compare'] = readCnf['Detect']['compare']
    # except Exception:
    #     print("Classification comparison is default")
    # logger.info('[%s] : [INFO] Classification comparison is %s',
    #             datetime.fromtimestamp(time.time()).strftime(log_format), settings['compare'])

    try:
        # print("Classification data generation using only anomalies set to %s" % readCnf['Detect']['anomalyOnly'])
        settings['anomalyOnly'] = readCnf['Detect']['anomalyOnly']
    except Exception:
        # print("Classification data generation using only anomalies set to False")
        pass
    logger.info('[%s] : [INFO] Classification data generation using only anomalies set to %s',
                datetime.fromtimestamp(time.time()).strftime(log_format), str(settings['anomalyOnly']))

    if settings["categorical"] is None:
        try:
            if not readCnf['Augmentation']['Categorical']:
                readCnf['Augmentation']['Categorical'] = None
                logger.info('[{}] : [INFO] Categorical columns defined as: {}'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format),
                    readCnf['Augmentation']['Categorical']))
            if readCnf['Augmentation']['Categorical'] == '0':
                settings["categorical"] = None
            else:
                settings["categorical"] = readCnf['Augmentation']['Categorical']
            logger.info('[%s] : [INFO] Categorical Features ->  %s',
                    datetime.fromtimestamp(time.time()).strftime(log_format),
                    settings['categorical'])
        except Exception:
            logger.warning('[%s] : [WARN] No Categorical Features selected from config file or comandline! Skipping encoding',
                           datetime.fromtimestamp(time.time()).strftime(log_format))
            settings["categorical"] = None
    else:
        logger.info('[%s] : [INFO] Categorical Features ->  %s',
                    datetime.fromtimestamp(time.time()).strftime(log_format), settings["categorical"])

    if not settings["point"]:
        try:
            settings['point'] = readCnf['Misc']['point']
            logger.info('[%s] : [INFO] Point  set to %s',
                        datetime.fromtimestamp(time.time()).strftime(log_format), settings['point'])
        except Exception:
            settings['point'] = 'False'
            logger.info('[%s] : [INFO] Point detection set to default %s',
                        datetime.fromtimestamp(time.time()).strftime(log_format), settings['point'])

    #print dmonC
    # sys.exit()
    # print("Conf file -> %s" %readCnf)
    # print("Settings  -> %s" %settings)

    engine = edengine.EDEngine(settings,
                                     dataDir=dataDir,
                                     modelsDir=modelsDir,
                                     queryDir=queryDir)
    #engine.printTest()
    engine.initConnector()
    if dask_backend:
        engine.runDask(engine)
    else:
        try:
            engine.runProcess(engine)
        except Exception as inst:
            logger.error('[{}] : [ERROR] Failed Process backend initialization with {} and {}'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format), type(inst), inst.args))
            logger.warning('[{}] : [WARN] Initializing default threaded engine, limited performance to be expected!'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format), type(inst), inst.args))
            engine.run(engine)

    logger.info('[{}] : [INFO] Exiting EDE framework'.format(
        datetime.fromtimestamp(time.time()).strftime(log_format)))


if __name__ == "__main__":
    def handler(singal_received, frame):
        logger.info('[{}] : [INFO] User break detected. Exiting EDE framework'.format(
        datetime.fromtimestamp(time.time()).strftime(log_format)))
        sys.exit(0)
    signal(SIGINT, handler)
    SchedulerEndpoint, Scale, SchedulerPort, EnforceCheck = check_dask_settings(cnf=sys.argv[1:])  # Todo Better solution
    if SchedulerEndpoint:
        if SchedulerEndpoint == "local":
            cluster = LocalCluster(n_workers=int(Scale))
            logger.info('[{}] : [INFO] Starting Dask local Cluster Backend with: {}'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format), cluster))
            client = Client(cluster)
            logger.info('[{}] : [INFO] Dask Client started with: {}'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format), client))
        else:
            scheduler_address = "{}:{}".format(SchedulerEndpoint, SchedulerPort)
            client = Client(address=scheduler_address)
            client.get_versions(check=EnforceCheck)
    else:
        cluster = 0
        client = 0
    main(sys.argv[1:],
         cluster,
         client)

