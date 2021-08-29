"""general file for utils"""

import yaml
import configparser

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


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
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

    # datetime date cols
    for date_col in ["date_created", "date_modified", "date_shipped"]:
        df[date_col + "_date"] = pd.to_datetime(df[date_col])
        df[date_col + "_date"] = df[date_col + "_date"].apply(lambda x: str(x).split(" ")[0])
        df[date_col + "_month"] = df[date_col + "_date"].apply(lambda x: "-".join(str(x).split(" ")[0].split("-")[:-1]))

    return df


def export_to_excel(outputs: dict, export_file_name: str):
    writer = pd.ExcelWriter(f"{export_file_name}.xlsx")
    for table in outputs:
        df = outputs[table]
        df.to_excel(writer, sheet_name=table)
    return writer.save()
