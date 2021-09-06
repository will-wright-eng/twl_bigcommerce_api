"""
## (2) MONTHLY REPORTS FOR INVENTORY VALUATION
- using [BigCommerce Catalog/Products v3 API](https://developer.bigcommerce.com/api-reference/store-management/catalog/products/getproducts) in BigCommProductsAPI class
"""

import numpy as np
import pandas as pd
import datetime as dt


def inventory_valuation_report_configs():
    """report inputs"""
    REPORT_TITLE = "MONTHLY REPORTS FOR INVENTORY VALUATION"

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