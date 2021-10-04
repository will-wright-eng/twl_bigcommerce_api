"""general file for utils"""

import os
import shutil

# import configparser
import datetime as dt
from pathlib import Path

import yaml
import boto3
import numpy as np
import pandas as pd

TODAY = str(dt.datetime.today()).split(" ")[0]
REPORT_FILE_PATH = os.path.join("xlsx_docs", TODAY)


def load_yml_configs(file_name: str) -> dict:
    with open(file_name, "r") as stream:
        try:
            configs = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return configs


# def load_config_file(config_part: str) -> dict:
#     config = configparser.ConfigParser()
#     config.read("project.cfg")
#     configs = dict(config.items(config_part))
#     return configs


def export_to_excel(outputs: dict, export_file_name: str):
    """https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html"""
    os.makedirs(REPORT_FILE_PATH, exist_ok=True)
    writer = pd.ExcelWriter(f"{REPORT_FILE_PATH}/{export_file_name}.xlsx")
    if "table_of_contents" in list(outputs):
        df = outputs["table_of_contents"]
        df.to_excel(writer, sheet_name="table_of_contents")
        outputs.pop("table_of_contents")

    for table in outputs:
        df = outputs[table]
        df.to_excel(writer, sheet_name=table)
    writer.save()
    return f"export to {export_file_name}.xlsx complete"


def upload_to_s3_v2(local_path: str, object_name: str, bucket_name: str =  os.getenv("S3_BUCKET")):
    """
    path_output: local dir file path
    bucket_name: name of s3 bucket
    key_path: key path + file name = object name
    """
    print(local_path, bucket_name, object_name)
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
    S3_BUCKET = os.getenv("S3_BUCKET")
    TODAY = str(dt.datetime.today()).split(" ")[0]
    file_name = f"{TODAY}_{data_table}.csv"
    folder = f"tmp_backup/backup_{data_table}"
    local_path = os.path.join(folder, file_name)
    object_name = f"backup_{data_table}/{file_name}"

    try:
        os.makedirs(folder, exist_ok=True)
        df.to_csv(local_path)
        resp = upload_to_s3_v2(
            local_path=local_path, bucket_name=S3_BUCKET, object_name=object_name
        )
    finally:
        shutil.rmtree("tmp_backup")
    return resp


def clean_string(string: str) -> str:
    string = "".join(e for e in string if e.isalnum() or e == " " or e=='/')
    string = string.replace("  ", " ").replace("  ", " ").replace(" ", "_")
    return string


def zip_process(file_or_dir: str) -> str:
    cwd = str(Path.cwd())
    zip_source = os.path.join(cwd, file_or_dir)
    zip_target = os.path.join(cwd, clean_string(file_or_dir))
    return shutil.make_archive(zip_target, "zip", zip_source)
