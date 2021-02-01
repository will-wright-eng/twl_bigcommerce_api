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
project_name = 'prod_backup_script'
logger = utilf.function_logger(logging.DEBUG,
                               logging.DEBUG,
                               function_name=project_name)

config = configparser.ConfigParser()
config.read('project.cfg')
configs = dict(config.items('s3_info'))
bucket_name = configs['bucket']
key_path = configs['prod_desc_records']

batch_file = cfg_dict['batch_file']
imgs_bool = cfg_dict['imgs_bool']
output_folder_html = cfg_dict['output_folder_html']
output_folder_combined = cfg_dict['output_folder_combined']
program_name = cfg_dict['program_name']


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
    folder = 'tables/'
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
    '''main docstring

    1. setup directory
    2. import product id list
    2. check overlap
    3. run cleanup process
    4. push files to s3
    '''

    logger.info('-- NEW JOB --')
    logger.info(batch_file)
    prod_ids = list(product_df(batch_file).product_id)
    batch_folder = batch_file.replace('.csv', '')

    # folders = [
    #     'results',
    #     'results/' + batch_folder,
    #     'results/' + batch_folder + '/' + output_folder_combined,
    #     'results/' + batch_folder + '/' + output_folder_html
    # ]
    # utilf.create_directory(folders, logger)

    # check outlap with previous batches
    overlap_list = check_batch_overlap(batch_file, prod_ids)
    if len(overlap_list) > 0:
        logger.info('overlapping = ' + str(overlap_list))
    prod_ids = [i for i in prod_ids if i not in overlap_list]

    logger.info('start process')
    base = base_api(project_name)
    res = {}

    for prod_id in prod_ids:
        logger.info('processing: ' + str(_id))
        json_data = base.get_prod(_id=prod_id)

        old_html = json_data['description']
        desc = clean_description(old_html, regex_dict, logger)
        d = desc.flight_chars_dict()
        new_html = desc.clean()

    #     _name = json_data['name']
    #     _sku = json_data['sku']
    #     _name = json_data['name']
    #     uid = str(_id) + '_' + _name + '_' + _sku

    #     _data = [
    #         _name, _sku, uid,old_html, new_html,
    #         len(re.findall('please note', new_html.lower())),
    #         len(re.findall('flight characteristics',new_html.lower())),
    #         len(re.findall('information about', new_html.lower()))
    #     ]
    #     _data_cols = [
    #         'id', 'name', 'sku', 'category', 'uid', 'old_html','new_html', 'count_please_note', 'count_flight_chars','count_info_about']

    #     if len(d) == 4:
    #         res[_id] = _data + [d[i] for i in d]
    #         flight_char_cols = [i for i in d]
    #     else:
    #         res[_id] = _data + [np.nan] * 4

    #     if imgs_bool:
    #         try:
    #             # videos incompatible with command line tool
    #             old_html = re.sub(
    #                 '<p><!-- mceItemMediaService.+?mceItemMediaService --></p>',
    #                 '', old_html)
    #             gen_preview_image(old_html, new_html, uid,
    #                               output_folder_combined,
    #                               output_folder_html)
    #         except OSError as e:
    #             logger.error('OSError: ' + str(e))

    # df = pd.DataFrame(res).T
    # df.reset_index(inplace=True)
    # df.columns = _data_cols + flight_char_cols
    # df['href_check'] = df.new_html.apply(lambda x: 'href' in x)
    # df.to_csv(batch_folder + '.csv', index=False)
    # logger.info(batch_folder + '.csv' + ' saved')

    # logger.info('file handling: zip directory and upload to s3')
    # remove output_folder_html from batch_folder folder
    # zip directory
    # temp_filename = 'temp.csv'
    # df.to_csv(temp_filename,index=False)
    # file_name = today+'_product_catalog.csv' # use existing nameing method

    # object_name = key_path+'/'+file_name
    # utilf.upload_to_s3(temp_filename, bucket_name, object_name, logger)

    # remove zip file and associated directory
    # https://stackoverflow.com/questions/6996603/how-to-delete-a-file-or-folder
    # os.remove(temp_filename)


if __name__ == '__main__':
    main()
