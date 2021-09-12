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


def remove_low_count_cols(df):
    meta = pd.DataFrame([list(df), df.dtypes, df.count()]).T
    meta.columns = ["col_name", "col_dtype", "col_count"]
    df = df[list(meta.loc[meta.col_count > 0.9 * len(meta)].col_name)]
    return df


def convert_datetime_cols(df: pd.DataFrame) -> pd.DataFrame:
    # datetime date cols
    for date_col in [i for i in list(df) if "date" in i]:
        df[date_col] = pd.to_datetime(df[date_col])
        df[date_col] = df[date_col].dt.tz_localize(None)
        df[date_col + "_date"] = df[date_col].apply(lambda x: str(x).split(" ")[0])
        df[date_col + "_month"] = df[date_col + "_date"].apply(lambda x: "-".join(str(x).split(" ")[0].split("-")[:-1]))
    return df


def clean_order_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # manual payment fill
    def null_fill(x):
        if x == "":
            return "Manual Payment"
        else:
            return x.title()

    df.payment_method = df.payment_method.apply(lambda x: null_fill(x))

    # amount columns set to float
    dollar_cols = [i for i in list(df) if "subtotal" in i] + [i for i in list(df) if "cost" in i]
    for col in dollar_cols:
        df[col] = df[col].astype(float)

    return convert_datetime_cols(df)


def top_level_category(ele):
    ele = ele.split("/")
    if len(ele) <= 1:
        return np.nan
    else:
        return ele[1]


def clean_product_dataframe(df: pd.DataFrame, base) -> pd.DataFrame:
    # join in brands table
    brand_df = base.get_brands()
    brand_df = brand_df[["id", "name"]]
    brand_df.columns = ["brand_id", "brand_name"]
    df = df.merge(brand_df, how="left", on="brand_id")

    # category from custom url
    df["category_all"] = ["/".join(i["url"].split("/")[:-2]) for i in list(df.custom_url)]
    df["category_top"] = df.category_all.apply(lambda x: top_level_category(x))

    float_cols = ["price", "cost_price", "inventory_level"]
    for col in float_cols:
        df[col] = df[col].astype(float)
    df["inventory_value"] = df["price"] * df["inventory_level"]
    df["inventory_value_by_cost"] = df["cost_price"] * df["inventory_level"]

    return convert_datetime_cols(df)


def export_to_excel(outputs: dict, export_file_name: str):
    """https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html"""
    TODAY = str(dt.datetime.today()).split(" ")[0]
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


def generate_report(df: pd.DataFrame, report_id: str = "testing", **configs) -> tuple:

    REPORT_TITLE = configs.get("report_title")
    input_dict = configs.get("input_dict")

    # ## API JSON standard
    # # top level
    # output_response = {}
    # data = []  # list of reports
    # meta = {}  # reports generated, sheets in each, and the table shapes

    # level 1
    report = {}
    report["id"] = 1
    report["type"] = "twl orders report"
    report["attributes"] = {
        "title": REPORT_TITLE,
        "input_settings": input_dict,
        "export_file_name": configs.get("export_file_name"),
    }
    report["tables"] = {}  # {'table1': pd.DataFrame, 'table2': pd.DataFrame, ...}

    ## generate report tables
    outputs = {}
    for table_name, inputs in input_dict.items():

        if inputs["type"] == "date_filter":
            df = df.loc[inputs["bool_op"](df[inputs["column"]], inputs["date"])]

        elif inputs["type"] == "pivot_table":
            table = pd.pivot_table(
                df,
                values=inputs["values"],
                index=inputs["index"],
                columns=inputs["columns"],
                aggfunc=np.sum,
            )
            table.columns = [j for i, j in list(table.columns)]
            outputs[table_name] = table

        elif inputs["type"] == "groupby_table":
            headers = {i: inputs["aggfuncs"] for i in inputs["values"]}
            table = df.groupby(inputs["index"]).agg(headers)
            # table.reset_index(inplace=True, drop=False)
            outputs[table_name] = table

        elif inputs["type"] == "sum_on_previous_table":
            tmp = pd.DataFrame(table.sum(axis=inputs["axis"]))
            tmp.columns = ["sum"]
            outputs[table_name] = tmp

    outputs["raw_data"] = df

    attributes = {}
    attributes["report_title"] = REPORT_TITLE
    tmp = {"table " + str(i): j for i, j in zip(range(len(list(outputs))), list(outputs))}
    attributes.update(tmp)
    tmp = pd.DataFrame(attributes.items())
    outputs["table_of_contents"] = tmp

    report["tables"] = outputs

    return report, attributes


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
