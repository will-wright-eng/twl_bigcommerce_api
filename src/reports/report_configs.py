from typing import List

import datetime as dt
from operator import lt, gt, eq


TODAY = str(dt.datetime.today()).split(" ")[0]
MONTH = str(dt.datetime.today().strftime("%b")).lower()
REPORT_START_DATE = "2021-09-01"


def sales_tax_report_configs() -> dict:
    """
    report type: orders
    """
    REPORT_TITLE = "ORDERS SUBTOTAL EX TAX BY PAYMENT METHOD"
    file_name = REPORT_TITLE.lower().replace(" ", "_")

    input_dict = {}

    inputs = {}
    inputs["type"] = "pivot_table"
    inputs["values"] = ["subtotal_ex_tax"]
    inputs["index"] = ["date_created_month"]
    inputs["columns"] = ["payment_method"]
    input_dict["ytd_pivot_by_month"] = inputs

    inputs = {}
    inputs["type"] = "data_filter"
    inputs["bool_arg"] = REPORT_START_DATE
    inputs["column"] = "date_created"
    inputs["bool_op"] = gt
    input_dict["table_modification"] = inputs

    inputs = {}
    inputs["type"] = "pivot_table"
    inputs["values"] = ["subtotal_ex_tax"]
    inputs["index"] = ["date_created_month", "date_created_date"]
    inputs["columns"] = ["payment_method"]
    input_dict[f"pivot_by_day_post_{MONTH}"] = inputs

    # inputs = {}
    # inputs["type"] = "pivot_table"
    # inputs["values"] = ["subtotal_ex_tax"]
    # inputs["index"] = ["date_created_month", "date_created_date"]
    # inputs["columns"] = ["base_shipping_cost"]
    # input_dict[f"pivot_shipping_by_day_post_{MONTH}"] = inputs

    inputs = {}
    inputs["type"] = "groupby_table"
    inputs["values"] = ["base_shipping_cost"]
    inputs["index"] = ["date_created_month", "date_created_date"]
    inputs["aggfuncs"] = ["sum", "count"]
    input_dict[f"pivot_shipping_by_day_post_{MONTH}"] = inputs

    inputs = {}
    inputs["type"] = "pivot_table"
    inputs["values"] = ["subtotal_ex_tax", "subtotal_inc_tax", "subtotal_tax"]
    inputs["index"] = ["date_created_month"]
    inputs["columns"] = ["payment_method"]
    input_dict[f"pivot_by_month_post_{MONTH}"] = inputs

    inputs = {}
    inputs["type"] = "sum_on_previous_table"
    inputs["axis"] = 1
    input_dict["sum_by_row"] = inputs

    inputs = {}
    inputs["type"] = "sum_on_previous_table"
    inputs["axis"] = 0
    input_dict["sum_by_column"] = inputs

    configs = {}
    configs["report_title"] = REPORT_TITLE
    configs["export_file_name"] = f"{TODAY}_{file_name}_post_{MONTH}"
    configs["input_dict"] = input_dict

    return configs


def sales_by_category_report_configs() -> dict:
    """
    report type: orders

    DONT INCLUDE BRAND OR CATEGORY COLUMNS
    """
    REPORT_TITLE = "ORDERS SUBTOTAL EX TAX BY CATEGORY AND BRAND"
    file_name = REPORT_TITLE.lower().replace(" ", "_")

    input_dict = {}

    inputs = {}
    inputs["type"] = "pivot_table"
    inputs["values"] = ["subtotal_ex_tax"]
    inputs["index"] = ["date_created_month"]
    inputs["columns"] = ["category_top"]
    input_dict["ytd_pivot_by_brand_and_categories"] = inputs

    inputs = {}
    inputs["type"] = "pivot_table"
    inputs["values"] = ["subtotal_ex_tax"]
    inputs["index"] = ["category_top", "category_all"]
    inputs["columns"] = ["date_created_month"]
    input_dict["ytd_pivot_by_categories"] = inputs

    inputs = {}
    inputs["type"] = "data_filter"
    inputs["bool_arg"] = REPORT_START_DATE
    inputs["column"] = "date_created"
    inputs["bool_op"] = gt
    input_dict["table_modification"] = inputs

    inputs = {}
    inputs["type"] = "pivot_table"
    inputs["values"] = ["subtotal_ex_tax"]
    inputs["index"] = ["date_created_month", "date_created_date"]
    inputs["columns"] = ["category_top"]
    input_dict["pivot_by_brand_and_date"] = inputs

    inputs = {}
    inputs["type"] = "pivot_table"
    inputs["values"] = ["subtotal_ex_tax"]
    inputs["index"] = ["category_top", "category_all"]
    inputs["columns"] = ["date_created_month"]
    input_dict["pivot_by_categories"] = inputs

    inputs = {}
    inputs["type"] = "sum_on_previous_table"
    inputs["axis"] = 1
    input_dict["sum_by_row"] = inputs

    inputs = {}
    inputs["type"] = "sum_on_previous_table"
    inputs["axis"] = 0
    input_dict["sum_by_column"] = inputs

    # TODAY = str(dt.datetime.today()).split(" ")[0]
    configs = {}
    configs["report_title"] = REPORT_TITLE
    configs["export_file_name"] = f"{TODAY}_{file_name}_post_{MONTH}"
    configs["input_dict"] = input_dict

    return configs


def inventory_valuation_report_configs() -> dict:
    """
    report type: product
    """
    REPORT_TITLE = "INVENTORY VALUATION REPORT"
    file_name = REPORT_TITLE.lower().replace(" ", "_")

    input_dict = {}

    inputs = {}
    inputs["type"] = "groupby_table"
    inputs["values"] = [
        "price",
        "cost_price",
        "inventory_level",
        "inventory_value",
        "inventory_value_by_cost",
    ]
    inputs["index"] = ["category_top"]
    inputs["aggfuncs"] = ["sum", "mean"]
    input_dict["groupby_category"] = inputs

    inputs = {}
    inputs["type"] = "groupby_table"
    inputs["values"] = [
        "price",
        "cost_price",
        "inventory_level",
        "inventory_value",
        "inventory_value_by_cost",
    ]
    inputs["index"] = ["category_top"]
    inputs["aggfuncs"] = "sum"
    input_dict["groupby_category_sum"] = inputs

    inputs = {}
    inputs["type"] = "groupby_table"
    inputs["values"] = [
        "price",
        "cost_price",
        "inventory_level",
        "inventory_value",
        "inventory_value_by_cost",
    ]
    inputs["index"] = ["category_top"]
    inputs["aggfuncs"] = ["sum", "mean", "median", "count"]
    input_dict["groupby_category"] = inputs

    inputs = {}
    inputs["type"] = "groupby_table"
    inputs["values"] = [
        "price",
        "cost_price",
        "inventory_level",
        "inventory_value",
        "inventory_value_by_cost",
    ]
    inputs["index"] = ["brand_name"]
    inputs["aggfuncs"] = "sum"
    input_dict["groupby_brand"] = inputs

    inputs = {}
    inputs["type"] = "groupby_table"
    inputs["values"] = [
        "price",
        "cost_price",
        "inventory_level",
        "inventory_value",
        "inventory_value_by_cost",
    ]
    inputs["index"] = ["brand_name", "category_top"]
    inputs["aggfuncs"] = "sum"
    input_dict["groupby_cat_and_brand"] = inputs

    inputs = {}
    inputs["type"] = "pivot_table"
    inputs["values"] = ["price"]
    inputs["index"] = ["brand_name", "category_top", "category_all"]
    inputs["columns"] = ["date_created_month"]
    input_dict["pivot_by_price"] = inputs

    inputs = {}
    inputs["type"] = "sum_on_previous_table"
    inputs["axis"] = 1
    input_dict["sum_by_row"] = inputs

    inputs = {}
    inputs["type"] = "sum_on_previous_table"
    inputs["axis"] = 0
    input_dict["sum_by_column"] = inputs

    # TODAY = str(dt.datetime.today()).split(" ")[0]
    configs = {}
    configs["report_title"] = REPORT_TITLE
    configs["export_file_name"] = f"{TODAY}_{file_name}"
    configs["input_dict"] = input_dict

    return configs


def collections_report_configs(collections: List[str]) -> dict:
    """
    report type: orders
    """
    REPORT_TITLE = "COLLECTIONS MONTHLY REPORT"
    file_name = REPORT_TITLE.lower().replace(" ", "_")

    input_dict = {}

    inputs = {}
    inputs["type"] = "pivot_table"
    inputs["values"] = ["price_ex_tax"]
    inputs["index"] = ["date_created_month"]
    inputs["columns"] = ["sku_prefix"]
    input_dict["ytd_pivot_by_month"] = inputs

    for sku_prefix in collections:
        inputs = {}
        inputs["type"] = "data_filter"
        inputs["bool_arg"] = sku_prefix
        inputs["column"] = "sku_prefix"
        inputs["bool_op"] = eq
        input_dict[f"data_filter_{sku_prefix.lower()}"] = inputs

        # inputs = {}
        # inputs["type"] = "pivot_table"
        # inputs["values"] = ["price_ex_tax"]
        # inputs["index"] = ["sku_prefix", "sku"]
        # inputs["columns"] = ["date_created_month"]
        # input_dict[f"pivot_by_month_{sku_prefix.lower()}"] = inputs

        inputs = {}
        inputs["type"] = "groupby_table"
        inputs["values"] = ["price_ex_tax"]
        inputs["index"] = ["date_created_month", "sku_prefix", "sku", "order_id"]
        inputs["aggfuncs"] = ["sum", "count"]
        input_dict[f"groupby_month_{sku_prefix.lower()}"] = inputs

        inputs = {}
        inputs["type"] = "data_reset"
        input_dict[f"data_reset_{sku_prefix.lower()}"] = inputs

    configs = {}
    configs["report_title"] = REPORT_TITLE
    configs["export_file_name"] = f"{TODAY}_{file_name}"
    configs["input_dict"] = input_dict

    return configs
