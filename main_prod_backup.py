'''docstring'''

import os
import http.client
import json
import logging
import inspect
import configparser
import datetime as dt

import pandas as pd

import modules.util_fxns as utilf
from modules.base_api import base_api

today = str(dt.date.today())
project_name = __file__.replace('.py', '')
logger = utilf.function_logger(logging.DEBUG,
                               logging.DEBUG,
                               function_name=project_name)

config = configparser.ConfigParser()
config.read('project.cfg')
configs = dict(config.items('s3_info'))
bucket_name = configs['bucket']
key_path = configs['backup_prods_key']


def main():
    '''main docsting'''
    logger.info('--NEW JOB--')
    base = base_api(project_name)
    df = base.get_all_prods()

    tempfile = 'temp.csv'
    df.to_csv(tempfile, index=False)

    upload_file = os.path.abspath(tempfile)
    file_name = today + '_product_catalog.csv'
    object_name = key_path + '/' + file_name
    utilf.upload_to_s3(upload_file, bucket_name, key_path, file_name, logger)

    os.remove(tempfile)


if __name__ == '__main__':
    main()
