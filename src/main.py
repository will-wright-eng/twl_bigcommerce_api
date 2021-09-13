"""main.py docstring

TODO:
- email reports
- add filter attributes to api calls
- github actions for autoformatting black -l 120 src/

API json response schema
https://jsonapi.org/

"""


import numpy as np
import pandas as pd

import utils.general as utils
import utils.dataframes as dfutils
import reports.pivot_report_configs as report_configs
from modules.bigcomm_api import BigCommOrdersAPI
from modules.bigcomm_api import BigCommProductsAPI

ANCHOR_DATE = "2021-01-01"


## PRODUCTS ##
def get_product_data() -> pd.DataFrame:
    base = BigCommProductsAPI()
    df = base.get_all()
    df = dfutils.clean_product_dataframe(df, base)
    return df


def generate_inventory_valuation_report(df: pd.DataFrame) -> str:
    # generate reports
    configs = report_configs.inventory_valuation_report_configs()
    report, attributes = dfutils.generate_report(df=df, **configs)
    # export
    df.drop(["description"], axis=1, inplace=True)
    status = utils.export_to_excel(outputs=report["tables"], export_file_name=report["attributes"]["export_file_name"])
    return status


## ORDERS ##
def get_orders_data() -> pd.DataFrame:
    base = BigCommOrdersAPI()
    tmp = base.get_all(min_date_modified=ANCHOR_DATE)

    dfs = []
    for ind, data in tmp.items():
        dfs.append(pd.DataFrame(data))

    df = pd.concat(dfs, axis=0)
    df = dfutils.clean_order_dataframe(df)
    return df, base


def generate_sales_tax_report(df: pd.DataFrame) -> str:
    # generate reports
    configs = report_configs.sales_tax_report_configs()
    report, attributes = dfutils.generate_report(df=df, **configs)
    # export
    status = utils.export_to_excel(outputs=report["tables"], export_file_name=report["attributes"]["export_file_name"])
    return status


def generate_sales_by_category_report(df: pd.DataFrame) -> str:
    # generate reports
    configs = report_configs.sales_by_category_report_configs()
    report, attributes = dfutils.generate_report(df=df, **configs)
    # export
    status = utils.export_to_excel(outputs=report["tables"], export_file_name=report["attributes"]["export_file_name"])
    return status


def generate_collections_report(df: pd.DataFrame, base) -> str:
    # get product details for each order
    tmp_df = base.create_order_lines_dataframe(df)

    # filter for collections
    collections = ["GMDIS", "GSC", "CPC", "KBC", "BRC"]
    tmp_df = tmp_df.loc[tmp_df.sku.str.contains("|".join(collections), case=False)]

    # merge in order details
    df = tmp_df.merge(df, how="left", left_on="order_id", right_on="id")

    # generate reports
    configs = report_configs.collections_report_configs(collections)
    report, attributes = dfutils.generate_report(df=df, **configs)
    # export
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

    df, base = get_orders_data()
    # backup orders
    data_table = "orders"
    utils.backup_dataframe(df, data_table)
    # orders reports
    orders_reports = [generate_sales_tax_report]#, generate_sales_by_category_report]
    for fxn in orders_reports:
        status = fxn(df)
        print(f"{fxn.__name__} ->", status)

    status = generate_collections_report(df, base)
    print(f"{generate_collections_report.__name__} ->", status)

    return status


if __name__ == "__main__":
    main()
