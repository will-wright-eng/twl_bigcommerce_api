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

from modules.bigcomm_api import BigCommOrdersAPI
from modules.bigcomm_api import BigCommProductsAPI

from utils.general import export_to_excel, clean_orders, generate_pivot_report
from reports.orders_reports import sales_tax_report_configs, sales_by_category_report_configs


def get_orders_data() -> pd.DataFrame:
    # get data
    base = BigCommOrdersAPI()
    tmp = base.get_all()

    dfs = []
    for ind, data in tmp.items():
        dfs.append(pd.DataFrame(data))

    df = pd.concat(dfs, axis=0)
    df = clean_orders(df)
    return df


def get_product_data() -> pd.DataFrame:
    # get data
    base = BigCommProductsAPI()
    df = base.get_all()

    # df = clean_dataframe(df)
    return df


def generate_sales_tax_report(df: pd.DataFrame) -> str:
    # generate reports
    configs = sales_tax_report_configs()
    report, attributes = generate_pivot_report(df=df, **configs)
    # export
    status = export_to_excel(outputs=report["tables"], export_file_name=report["attributes"]["export_file_name"])
    return status


if __name__ == "__main__":
    df = get_orders_data()
    status = generate_sales_tax_report(df)
    print(status)
