"""general file for utils"""

import os
import yaml

import shutil
import configparser
import datetime as dt

import boto3
import numpy as np
import pandas as pd


def load_yml_configs(file_name: str) -> dict:
    with open(file_name, "r") as stream:
        try:
            configs = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return configs


def load_config_file(config_part: str) -> dict:
    config = configparser.ConfigParser()
    config.read("project.cfg")
    configs = dict(config.items(config_part))
    return configs


def export_to_excel(outputs: dict, export_file_name: str):
    """https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html"""
    TODAY = str(dt.datetime.today()).split('.')[0].replace(' ','_').replace(':','')
    file_path = os.path.join("xlsx_docs", TODAY)
    os.makedirs(file_path, exist_ok=True)
    writer = pd.ExcelWriter(f"{file_path}/{export_file_name}.xlsx")
    if "table_of_contents" in list(outputs):
        df = outputs["table_of_contents"]
        df.to_excel(writer, sheet_name="table_of_contents")
        outputs.pop("table_of_contents")

    for table in outputs:
        df = outputs[table]
        df.to_excel(writer, sheet_name=table)
    writer.save()
    return f"export to {export_file_name}.xlsx complete"


def upload_to_s3_v2(local_path: str, bucket_name: str, object_name: str):
    """
    path_output: local dir file path
    bucket_name: name of s3 bucket
    key_path: key path + file name = object name
    """
    s3 = boto3.client("s3")
    response = s3.upload_file(local_path, bucket_name, object_name)
    return response


def backup_dataframe(df: pd.DataFrame, data_table: str):
    """
    - generates tmp folders
    - saves csv
    - exports to S3 bucket
    - deletes tmp directory
    """
    S3_BUCKET = "twl-dev"
    TODAY = str(dt.datetime.today()).split(" ")[0]
    file_name = f"{TODAY}_{data_table}.csv"
    folder = f"tmp_backup/backup_{data_table}"
    local_path = os.path.join(folder, file_name)
    object_name = f"backup_{data_table}/{file_name}"

    try:
        os.makedirs(folder, exist_ok=True)
        df.to_csv(local_path)
        resp = upload_to_s3_v2(local_path=local_path, bucket_name=S3_BUCKET, object_name=object_name)
    finally:
        shutil.rmtree("tmp_backup")
    return resp
