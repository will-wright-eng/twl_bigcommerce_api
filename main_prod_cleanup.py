'''docstring'''

import re
import os
import sys
import http.client
import json
import logging
import inspect
import configparser
import datetime as dt

import numpy as np
import pandas as pd
import imgkit
from PIL import Image

import modules.util_fxns as utilf
from modules.base_api import base_api
from modules.regex_dict import regex_dict
from modules.clean_description import clean_description

today = str(dt.date.today())
# project_name = 'prod_backup_script'
project_name = __file__.replace('.py','')
logger = utilf.function_logger(logging.DEBUG,
                               logging.DEBUG,
                               function_name=project_name)

config = configparser.ConfigParser()
config.read('project.cfg')
# configs = dict(config.items('s3_info'))
# bucket_name = configs['bucket']
# key_path = configs['prod_desc_records']

configs = dict(config.items('desc_cleanup'))
batch_file = configs['batch_file']
# imgs_bool = cfg_dict['imgs_bool']
# output_folder_html = cfg_dict['output_folder_html']
# output_folder_combined = cfg_dict['output_folder_combined']
# program_name = cfg_dict['program_name']


def gen_preview_image(old_html, new_html, uid, output_folder_combined,
                      output_folder_html):
    '''docstring for gen_preview_image'''
    image_names = [
        output_folder_html + '/' + uid + '_old.png',
        output_folder_html + '/' + uid + '_new.png'
    ]
    imgkit.from_string(old_html, image_names[0])
    imgkit.from_string(new_html, image_names[1])
    images = [Image.open(x) for x in image_names]
    widths, heights = zip(*(i.size for i in images))
    total_width = max(widths)
    max_height = sum(heights) + 10
    new_im = Image.new('RGB', (total_width, max_height))
    offset = 0
    for im in images:
        new_im.paste(im, (0, offset))
        offset += im.size[1] + 10
    new_im.save(output_folder_combined + '/' + uid + '.png')


def check_batch_overlap(batch_file, batch_prod_ids):
    '''check_batch_overlap docstring'''
    folder = 'batches/'
    files = [i for i in os.listdir(folder) if 'products-20' in i]
    exclude_batch = batch_file.split('/')[-1]
    files = [i for i in files if i != exclude_batch]
    prod_ids = []
    for file in files:
        df = pd.read_csv(folder + file)
        df = df.loc[df['Product Type'] == 'P']
        prod_id = list(df['Product ID'])
        prod_ids.append(prod_id)
    ids = [int(j) for i in prod_ids for j in i]
    res = []
    for prod_id in batch_prod_ids:
        prod_id = int(prod_id)
        if prod_id in ids:
            logger.warn('WARNING: overlapping id found: ' + str(prod_id))
            res.append(prod_id)
    return res


def main():
    '''main docstring'''
    logger.info('-- NEW JOB --')
    logger.info(batch_file)
    prod_ids = list(utilf.product_df('batches/'+batch_file).product_id)
    batch_folder = batch_file.replace('.csv', '')

    # check outlap with previous batches
    overlap_list = check_batch_overlap(batch_file, prod_ids)
    if len(overlap_list) > 0:
        logger.info('overlapping = ' + str(overlap_list))
    prod_ids = [i for i in prod_ids if i not in overlap_list]

    logger.info('start process')
    base = base_api(project_name)
    res = {}

    for prod_id in prod_ids:
        logger.info('processing: ' + str(prod_id))
        json_data = base.get_prod(_id=prod_id)
        # print(type(json_data),list(json_data))
        old_html = json_data['description'].replace('\r\n\r\n',' ').replace('\r\n',' ').replace('\\','')

        # print('isinstance(old_html, str) == ',isinstance(old_html, str))
        # print(regex_dict)
        # print(old_html)
        desc_obj = clean_description(old_html, regex_dict, logger)
        # d = desc_obj.flight_chars_dict()
        new_html = desc_obj.clean()
        logger.info('modifying ' + str(prod_id) + ' within BigCommerce')
        base.put_prod_desc(new_html, _id=prod_id)

        res[prod_id] = [prod_id,old_html,new_html]
    pd.DataFrame(res).to_csv('test.csv')

if __name__ == '__main__':
    main()
