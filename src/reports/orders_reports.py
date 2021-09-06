"""
## (1) MONTHLY REPORT OF SALES FOR SALES TAX PURPOSES BY PAYMENT METHOD
- using [BigCommerce Orders v2 API](https://developer.bigcommerce.com/api-reference/store-management/orders/orders/getallorders) in BigCommOrdersAPI class

## (3) NEED A MONTHLY SALES REPORT BY CATEGORY AND BY ITEM.
- using [BigCommerce Orders v2 API](https://developer.bigcommerce.com/api-reference/store-management/orders/orders/getallorders) in BigCommOrdersAPI class
"""

import numpy as np
import pandas as pd
import datetime as dt


def sales_tax_report_configs():
    """report inputs"""
    REPORT_TITLE = "SUBTOTAL EXCLUDING TAX BY DATE CREATED AND PAYMENT METHOD"

    input_dict = {}

    inputs = {}
    inputs["values"] = ["subtotal_ex_tax"]
    inputs["index"] = ["date_created_month", "date_created_date"]
    inputs["columns"] = ["payment_method"]
    input_dict["pivot_by_day"] = inputs

    inputs = {}
    inputs["values"] = ["subtotal_ex_tax", "subtotal_inc_tax", "subtotal_tax"]
    inputs["index"] = ["date_created_month"]
    inputs["columns"] = ["payment_method"]
    input_dict["pivot_by_month"] = inputs

    TODAY = str(dt.datetime.today()).split(" ")[0]
    configs = {}
    configs["report_title"] = REPORT_TITLE
    configs["export_file_name"] = f"{TODAY}_sales_tax_report_post_aug01"
    configs["input_dict"] = input_dict
    return configs


def sales_by_category_report_configs():
    """report inputs"""
    REPORT_TITLE = "SALES REPORT BY CATEGORY AND BY ITEM"

    input_dict = {}

    inputs = {}
    inputs["values"] = ["subtotal_ex_tax"]
    inputs["index"] = ["date_created_month", "date_created_date"]
    inputs["columns"] = ["payment_method"] #<-- EDIT
    input_dict["pivot_by_day"] = inputs

    inputs = {}
    inputs["values"] = ["subtotal_ex_tax", "subtotal_inc_tax", "subtotal_tax"]
    inputs["index"] = ["date_created_month"]
    inputs["columns"] = ["payment_method"] #<-- EDIT
    input_dict["pivot_by_month"] = inputs

    TODAY = str(dt.datetime.today()).split(" ")[0]
    configs = {}
    configs["report_title"] = REPORT_TITLE
    configs["export_file_name"] = f"{TODAY}_sales_tax_report_post_aug01"
    configs["input_dict"] = input_dict
    return configs

def generate_pivot_report(
    df: pd.DataFrame, report_id: str = "testing", **configs
) -> tuple:

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

    ## generate report
    outputs = {}
    for table_name, inputs in input_dict.items():
        table = pd.pivot_table(
            df,
            values=inputs["values"],
            index=inputs["index"],
            columns=inputs["columns"],
            aggfunc=np.sum,
        )
        table.columns = [j for i, j in list(table.columns)]
        outputs[table_name] = table

    ## suppliemental tables -- based on last input table
    #
    tmp = pd.DataFrame(table.sum(axis=1))
    tmp.columns = ["sum"]
    outputs["sum_by_row"] = tmp

    #
    tmp = pd.DataFrame(table.sum(axis=0))
    tmp.columns = ["sum"]
    outputs["sum_by_column"] = tmp

    outputs["raw_data"] = df

    #
    attributes = {}
    attributes["report_title"] = REPORT_TITLE
    tmp = {
        "table " + str(i): j for i, j in zip(range(len(list(outputs))), list(outputs))
    }
    attributes.update(tmp)
    tmp = pd.DataFrame(attributes.items())
    outputs["table_of_contents"] = tmp

    report["tables"] = outputs

    return report, attributes
