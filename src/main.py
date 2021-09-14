"""main.py docstring

TODO:
- fix sales by category report! bring category and/or brand into orders

- email reports
- add filter attributes to api calls
- github actions for autoformatting black -l 120 src/
- automate to run on monthly basis

API json response schema
https://jsonapi.org/
"""


import numpy as np
import pandas as pd

import utils.general as utils
import utils.dataframes as dfutils
import reports.report_logic as reports
from modules.bigcomm_api import BigCommOrdersAPI
from modules.bigcomm_api import BigCommProductsAPI

ANCHOR_DATE = "2021-01-01"


## PRODUCTS ##
def get_product_data() -> pd.DataFrame:
    base = BigCommProductsAPI()
    df = base.get_all()
    df = dfutils.clean_product_dataframe(df, base)
    return df


## ORDERS ##
def get_orders_data() -> pd.DataFrame:
    base = BigCommOrdersAPI()
    tmp = base.get_all(min_date_modified=ANCHOR_DATE)

    dfs = []
    for ind, data in tmp.items():
        dfs.append(pd.DataFrame(data))

    df = pd.concat(dfs, axis=0)
    df = dfutils.clean_order_dataframe(df)
    df = df.loc[df.date_created > ANCHOR_DATE]
    return df, base


def main():
    df = get_product_data()
    # backup products
    data_table = "product_catalog"
    utils.backup_dataframe(df, data_table)
    # product reports
    product_reports = [reports.generate_inventory_valuation_report]
    for fxn in product_reports:
        status = fxn(df)
        print(f"{fxn.__name__} -> {status}")

    df, base = get_orders_data()
    # backup orders
    data_table = "orders"
    utils.backup_dataframe(df, data_table)
    # orders reports
    orders_reports = [reports.generate_sales_tax_report]  # , generate_sales_by_category_report]
    for fxn in orders_reports:
        status = fxn(df)
        print(f"{fxn.__name__} -> {status}")

    status = reports.generate_collections_report(df, base)
    print(f"{reports.generate_collections_report.__name__} -> {status}")

    return status


if __name__ == "__main__":
    main()
