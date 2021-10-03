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
# REPORT_START_DATE = "2021-09-01" --> see report_configs.py


def get_product_data() -> pd.DataFrame:
    base = BigCommProductsAPI()
    df = base.get_all()
    df = dfutils.clean_product_dataframe(df=df, base=base)
    return df, base


def get_orders_data() -> pd.DataFrame:
    base = BigCommOrdersAPI()
    tmp = base.get_all(min_date_modified=ANCHOR_DATE)

    dfs = []
    for ind, data in tmp.items():
        dfs.append(pd.DataFrame(data))

    df = pd.concat(dfs, axis=0)
    df = dfutils.clean_order_dataframe(df=df)
    df = df.loc[df.date_created > ANCHOR_DATE]
    return df, base


def main():

    df, base = get_product_data()
    data_table = "product_catalog"
    utils.backup_dataframe(df=df, data_table=data_table)
    product_reports = [reports.generate_inventory_valuation_report]
    for fxn in product_reports:
        status = fxn(df)
        print(f"{fxn.__name__} -> {status}")
    base.close_conn()

    df, base = get_orders_data()
    data_table = "orders"
    utils.backup_dataframe(df=df, data_table=data_table)
    orders_reports = [
        reports.generate_sales_tax_report
    ]  # , generate_sales_by_category_report]
    for fxn in orders_reports:
        status = fxn(df)
        print(f"{fxn.__name__} -> {status}")
    status = reports.generate_collections_report(df=df, base=base)
    print(f"{reports.generate_collections_report.__name__} -> {status}")
    base.close_conn()

    # zip reports folder and upload to s3
    zip_file = zip_process(file_or_dir=utils.REPORT_FILE_PATH)
    utils.upload_to_s3_v2(
        local_path=zip_file,
        bucket_name=os.getenv("S3_BUCKET"),
        object_name=zip_file.replace(".zip", "_reports.zip"),
    )


if __name__ == "__main__":
    main()
