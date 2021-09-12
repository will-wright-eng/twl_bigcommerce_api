"""main.py docstring

reports_list = ['inventory valuation','collections report','sales tax report']
main(): run reports list

Version 1:
- product and orders classes will pull information from api
- apply_filters method --> output: list of dataframes
- write_to_excel method

TODO:
- email reports
- add filter attributes to api calls
- github actions for autoformatting via black -l 120 src/

API json response schema
https://jsonapi.org/

"""


import numpy as np
import pandas as pd

import utils.general as utils
import reports.pivot_report_configs as report_configs
from modules.bigcomm_api import BigCommOrdersAPI
from modules.bigcomm_api import BigCommProductsAPI

ANCHOR_DATE = "2021-01-01"


def get_orders_data() -> pd.DataFrame:
    base = BigCommOrdersAPI()
    tmp = base.get_all(min_date_modified=ANCHOR_DATE)

    dfs = []
    for ind, data in tmp.items():
        dfs.append(pd.DataFrame(data))

    df = pd.concat(dfs, axis=0)
    df = utils.clean_order_dataframe(df)
    return df


def get_product_data() -> pd.DataFrame:
    base = BigCommProductsAPI()
    df = base.get_all()
    df = utils.clean_product_dataframe(df, base)
    return df


def generate_sales_tax_report(df: pd.DataFrame) -> str:
    # generate reports
    configs = report_configs.sales_tax_report_configs()
    report, attributes = utils.generate_report(df=df, **configs)
    # export
    status = utils.export_to_excel(outputs=report["tables"], export_file_name=report["attributes"]["export_file_name"])
    return status


def generate_sales_by_category_report(df: pd.DataFrame) -> str:
    # generate reports
    configs = report_configs.sales_by_category_report_configs()
    report, attributes = utils.generate_report(df=df, **configs)
    # export
    status = utils.export_to_excel(outputs=report["tables"], export_file_name=report["attributes"]["export_file_name"])
    return status


def generate_inventory_valuation_report(df: pd.DataFrame) -> str:
    # generate reports
    configs = report_configs.inventory_valuation_report_configs()
    report, attributes = utils.generate_report(df=df, **configs)
    # export
    df.drop(["description"], axis=1, inplace=True)
    status = utils.export_to_excel(outputs=report["tables"], export_file_name=report["attributes"]["export_file_name"])
    return status


def main():
    df = get_product_data()
    # backup products
    data_table = "product_catalog"
    utils.backup_dataframe(df, data_table)
    # product reports
    product_reports = [generate_inventory_valuation_report]
    for fxn in product_reports:
        status = fxn(df)
        print(f"{fxn.__name__} ->", status)

    df = get_orders_data()
    # backup orders
    data_table = "orders"
    utils.backup_dataframe(df, data_table)
    # orders reports
    orders_reports = [generate_sales_tax_report, generate_sales_by_category_report]  # generate_collection_report
    for fxn in product_reports:
        status = fxn(df)
        print(f"{fxn.__name__} ->", status)

    return status


if __name__ == "__main__":
    main()
