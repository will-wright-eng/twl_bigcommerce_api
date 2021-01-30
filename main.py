'''docstring'''

import http.client
import json
import logging
import inspect
import configparser

import pandas as pd

import modules.util_fxns as utilf
from modules.base_api import base_api

project_name = 'twl_bc_api'
logger = utilf.function_logger(logging.DEBUG,
                               logging.DEBUG,
                               function_name=project_name)


def convert_pages_to_df(data):
    dfs = []
    for page in data:
        logger.info(str(page))
        df = pd.DataFrame(data[page]['data'])
        dfs.append(df)
    df = pd.concat(dfs)
    return df


def main():
    base = base_api(project_name)
    df = convert_pages_to_df(base.get_all_prods())
    df.to_csv('test.csv', index=False)


if __name__ == '__main__':
    main()
