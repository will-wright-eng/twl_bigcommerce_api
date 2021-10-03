"""
report logic docstring
- contains top level logic for generating reports
"""


import numpy as np
import pandas as pd

import utils.general as utils
import utils.dataframes as dfutils
import reports.report_configs as report_configs
from modules.bigcomm_api import BigCommOrdersAPI


## PRODUCTS ##
def generate_inventory_valuation_report(df: pd.DataFrame) -> str:
    # generate reports
    configs = report_configs.inventory_valuation_report_configs()
    report, attributes = dfutils.generate_report(df=df, **configs)
    # export
    df.drop(["description"], axis=1, inplace=True)
    status = utils.export_to_excel(
        outputs=report["tables"],
        export_file_name=report["attributes"]["export_file_name"],
    )
    return status


## ORDERS ##
def generate_sales_tax_report(df: pd.DataFrame) -> str:
    # generate reports
    configs = report_configs.sales_tax_report_configs()
    report, attributes = dfutils.generate_report(df=df, **configs)
    # export
    status = utils.export_to_excel(
        outputs=report["tables"],
        export_file_name=report["attributes"]["export_file_name"],
    )
    return status


def generate_sales_by_category_report(df: pd.DataFrame) -> str:
    # generate reports
    configs = report_configs.sales_by_category_report_configs()
    report, attributes = dfutils.generate_report(df=df, **configs)
    # export
    status = utils.export_to_excel(
        outputs=report["tables"],
        export_file_name=report["attributes"]["export_file_name"],
    )
    return status


def generate_collections_report(df: pd.DataFrame, base: BigCommOrdersAPI) -> str:
    # get product details for each order
    tmp_df = base.create_order_lines_dataframe(df)

    # filter for collections
    collections = ["GMDIS", "GSC", "CPC", "KBC", "BRC"]
    tmp_df = tmp_df.loc[tmp_df.sku.str.contains("|".join(collections), case=False)]

    # merge in order details
    df = tmp_df.merge(df, how="left", left_on="order_id", right_on="id")
    utils.backup_dataframe(df, "order_lines")

    # generate reports
    configs = report_configs.collections_report_configs(collections)
    report, attributes = dfutils.generate_report(df=df, **configs)
    # export
    status = utils.export_to_excel(
        outputs=report["tables"],
        export_file_name=report["attributes"]["export_file_name"],
    )
    return status
