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

# from weka.core.converters import Loader, Saver
from os import listdir
import sys
from os.path import isfile, join
from edelogger import logger
import yaml
import getopt
from functools import wraps
import os
import csv
import pandas as pd
from datetime import datetime
import time
import numpy as np


modelDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')


# def convertCsvtoArff(indata, outdata):
#     '''
#     :param indata: -> input csv file
#     :param outdata: -> output file
#     :return:
#     '''
#     loader = Loader(classname="weka.core.converters.CSVLoader")
#     data = loader.load_file(indata)
#     saver = Saver(classname="weka.core.converters.ArffSaver")
#     saver.save_file(data, outdata)

log_format = '%Y-%m-%d %H:%M:%S'

def queryParser(query):
    '''
    :param query: -> query of the form  {"Query": "yarn:resourcemanager, clustre, jvm_NM;system"}
    :return: -> dictionary of the form {'system': 0, 'yarn': ['resourcemanager', 'clustre', 'jvm_NM']}
    '''
    type = {}
    for r in query.split(';'):
        if r.split(':')[0] == 'yarn':
            try:
                type['yarn'] = r.split(':')[1].split(', ')
            except Exception:
                type['yarn'] = 0
        if r.split(':')[0] == 'spark':
            try:
                type['spark'] = r.split(':')[1].split(', ')
            except Exception:
                type['spark'] = 0
        if r.split(':')[0] == 'storm':
            try:
                type['storm'] = r.split(':')[1].split(', ')
            except Exception:
                type['storm'] = 0
        if r.split(':')[0] == 'system':
            try:
                type['system'] = r.split(':')[1].split(', ')
            except Exception:
                type['system'] = 0
        if r.split(':')[0] == 'cassandra':
            try:
                type['cassandra'] = r.split(':')[1].split(', ')
            except Exception:
                type['cassandra'] = 0
        if r.split(':')[0] == 'mongodb':
            try:
                type['mongodb'] = r.split(':')[1].split(', ')
            except Exception:
                type['mongodb'] = 0
        if r.split(':')[0] == 'userquery':
            type['userquery'] = 0
        if r.split(':')[0] == 'cep':
            type['cep'] = 0
    return type


def nodesParse(nodes):
    if not nodes:
        return 0
    return nodes.split(';')


def getModelList():
    '''
    :return: -> returns the current list of saved models
    '''
    onlyfiles = [f for f in listdir(modelDir) if isfile(join(modelDir, f))]
    return onlyfiles


def csvheaders2colNames(csvfile, adname):
    '''
    :param csvfile: -> input csv or dataframe
    :param adname: -> string to add to column names
    :param df: -> if set to false csvfile is used if not df is used
    :return:
    '''
    colNames = {}
    if isinstance(csvfile, str):
        with open(csvfile, 'rb') as f:
            reader = csv.reader(f)
            i = next(reader)
        i.pop
        for e in i:
            if e == 'key':
                pass
            else:
                colNames[e] = '%s_%s' %(e, adname)
    elif isinstance(csvfile, pd.DataFrame):
        for e in csvfile.columns.values:
            if e =='key':
                pass
            else:
                colNames[e] = '%s_%s' % (e, adname)
    else:
        return 0
    return colNames


def str2Bool(st):
    '''
    :param st: -> string to test
    :return: -> if true then returns 1 else 0
    '''
    if type(st) is bool:
        return st
    if st in ['True', 'true', '1']:
        return 1
    elif st in ['False', 'false', '0']:
        return 0
    else:
        return 0


def cfilterparse(filter):
    if isinstance(filter, list):
        return filter
    if isinstance(filter, dict):
        try:
            drop_file_loc = filter['Dlist']
        except Exception as inst:
            logger.error('[{}] : [ERROR] Invalid key found in Filter DColumns: {}'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format), inst.args))
            sys.exit(0)
        if checkFile(drop_file_loc):
            with open(drop_file_loc) as stream:
                try:
                    filter_list = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    logger.error('[{}] : [ERROR] YAML DColumns file parse error with {} and {}'.format(
                        datetime.fromtimestamp(time.time()).strftime(log_format), type(exc), exc.args))
                    sys.exit(1)
                # print(filter_list)
                return filter_list
        else:
            logger.error('[{}] : [ERROR] File not found for DColumns at: {}'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format), drop_file_loc))
            sys.exit(1)
    return filter.split(';')


def rfilterparse(filter):
    ld = 0
    gd = 0
    if isinstance(filter, dict):
        ld = filter['ld']
        gd = filter['gd']
    else:
        for e in filter.split(';'):
            if e.split(':')[0] == 'ld':
                ld = e.split(':')[1]
            if e.split(':')[0] == 'gd':
                gd = e.split(':')[1]
    return ld, gd


def assertFrameEqual(df1, df2, **kwds):
    """ Assert that two dataframes are equal, ignoring ordering of columns"""
    from pandas.util.testing import assert_frame_equal
    return assert_frame_equal(df1.fillna(1).sort_index(axis=1), df2.fillna(1).sort_index(axis=1), check_names=True, **kwds)


def testDF(dataDir, csv1, csv2):
    '''
    :param dataDir: -> data directory
    :param csv1: -> input csv1
    :param csv2: -> input csv2
    :return:
    '''
    test1 = pd.read_csv(os.path.join(dataDir, csv1))
    test2 = pd.read_csv(os.path.join(dataDir, csv2))

    print(len(set(test1.columns.values)))
    print(len(set(test2.columns.values)))
    A = set(pd.read_csv(os.path.join(dataDir, csv1), index_col=False, header=None)[
                0])  # reads the csv, takes only the first column and creates a set out of it.
    B = set(pd.read_csv(os.path.join(dataDir, csv2), index_col=False, header=None)[0])  # same here
    print((A - B))  # set A - set B gives back everything thats only in A.
    print((B - A))
    t1 = test1.sort_index(axis=1)
    t2 = test2.sort_index(axis=1)

    t1.to_csv(os.path.join(dataDir, 'cTest1.csv'))
    t2.to_csv(os.path.join(dataDir, 'cTest2.csv'))
    if t1.equals(t2):
        print("DF's are equal")
    else:
        print("DF's are not equal")


def pointThraesholds(thresholds):
    '''
    :param thresholds: -> string that defines threashold for system metrics
    :return: -> dictionary with parsed thresholds
    '''
    if thresholds == 'default':
        return 0
    if not thresholds:
        return 0
    if thresholds == ' ':
        return 0
    th = {}
    for el in thresholds.split(';'):
        th[el.split(':')[0]] = {'bound': el.split(':')[1], 'threashold': el.split(':')[2]}
    return th


def parseDelay(st):
    '''
    :param st: -> string containing delay
    :return: -> number of seconds
    '''
    if 's' == st[-1:]:
        return int(st[:-1])
    elif 'm' == st[-1:]:
        return int(st[:-1])*60
    elif 'h' == st[-1:]:
        return int(st[:-1]) * 3600
    else:
        return 0


def ut2hum(ut):
    htime = datetime.fromtimestamp(ut / 1000).strftime(log_format)
    if "1970" in htime:
        htime = datetime.fromtimestamp(ut).strftime(log_format)
    return htime


def parseMethodSettings(st):
    if st == 'default':
        return 0
    mSettings = []
    for k, v in st.items():
        if len(k) > 1:
            ak = k
        else:
            ak = k.upper()
        mSettings.append("-%s" % ak)
        mSettings.append(v)
    return mSettings


def wait4Model(count=0):
    test = False
    if test or count < 10:
        time.sleep(1)
        count += 1
        return wait4Model(count)
    return 1


def checkFile(file):
    if os.path.isfile(file):
        return 1
    else:
        return 0


def check_dask_settings(cnf=None):
    if cnf is None:
        cnf_file = 'ede_config.yaml'
    try:
        opts, args = getopt.getopt(cnf, "he:tf:m:vx:d:lq:", ["endpoint=", "file=", "method=", "export=", "detect=", "query="])
    except getopt.GetoptError:
        logger.warning('[%s] : [WARN] Invalid argument received exiting', datetime.fromtimestamp(time.time()).strftime(log_format))
        print("ede.py -f <filelocation>, -t -m <method> -v -x <modelname>")
        sys.exit(0)
    for opt, arg in opts:
        if opt in ("-f", "--file"):
            cnf_file = arg
    try:
        with open(cnf_file) as cf:
            readCnf = yaml.unsafe_load(cf)
        SchedulerEndpoint = readCnf['Connector']['Dask']['SchedulerEndpoint']
        Scale = readCnf['Connector']['Dask']['Scale']
        SchedulerPort = readCnf['Connector']['Dask']['SchedulerPort']
        EnforceCheck = readCnf['Connector']['Dask']['EnforceCheck']
    except Exception:
        SchedulerEndpoint = 0
        Scale = 0
        SchedulerPort = 0
        EnforceCheck = 0
    return SchedulerEndpoint, Scale, SchedulerPort, EnforceCheck


def check_valid(*args, **kwargs):
    def inner(func):
        if kwargs['endpont'] is None:
            logger.error('[{}] : [ERROR] Endpoint not defined in config'.format(
                datetime.fromtimestamp(time.time()).strftime(log_format)))
            sys.exit(1)
        else:
            return func
    return inner

def check_valid2(f, end):
    def wrapper(*args):
        if end is None:
            print("None detected")
        else:
            return f(*args)
    return wrapper()


def revers_oh(y_oh):
    """
    One hot decoding for DNN
    :param y_oh: one hot encoded gorund truth or prediction
    :return: decoded y_oh
    """
    decode = []
    for r in y_oh:
        result = np.where(r==1.)[0]
        # check if network assigned more than one or non labels
        if len(result) > 1 or len(result) == 0:
            if len(result) > 1:
                result = np.array(result[0])  # select first class
            elif len(result) == 0:
                result = np.array[0]
        decode.append(result[0])
    return decode





