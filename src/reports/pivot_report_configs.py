"""
## (1) MONTHLY REPORT OF SALES FOR SALES TAX PURPOSES BY PAYMENT METHOD
- using [BigCommerce Orders v2 API](https://developer.bigcommerce.com/api-reference/store-management/orders/orders/getallorders) in BigCommOrdersAPI class


## (2) MONTHLY REPORTS FOR INVENTORY VALUATION
- using [BigCommerce Catalog/Products v3 API](https://developer.bigcommerce.com/api-reference/store-management/catalog/products/getproducts) in BigCommProductsAPI class


## (3) NEED A MONTHLY SALES REPORT BY CATEGORY AND BY ITEM.
- using [BigCommerce Orders v2 API](https://developer.bigcommerce.com/api-reference/store-management/orders/orders/getallorders) in BigCommOrdersAPI class
"""


import datetime as dt
from operator import lt, gt, eq


REPORT_START_DATE = "2021-08-01"


def sales_tax_report_configs():
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
    inputs["type"] = "date_filter"
    inputs["date"] = REPORT_START_DATE
    inputs["column"] = "date_created"
    inputs["bool_op"] = gt
    input_dict["table_modification"] = inputs

    inputs = {}
    inputs["type"] = "pivot_table"
    inputs["values"] = ["subtotal_ex_tax"]
    inputs["index"] = ["date_created_month", "date_created_date"]
    inputs["columns"] = ["payment_method"]
    input_dict["pivot_by_day_post_aug01"] = inputs

    inputs = {}
    inputs["type"] = "pivot_table"
    inputs["values"] = ["subtotal_ex_tax", "subtotal_inc_tax", "subtotal_tax"]
    inputs["index"] = ["date_created_month"]
    inputs["columns"] = ["payment_method"]
    input_dict["pivot_by_month_post_aug01"] = inputs

    inputs = {}
    inputs["type"] = "sum_on_previous_table"
    inputs["axis"] = 1
    input_dict["sum_by_row"] = inputs

    inputs = {}
    inputs["type"] = "sum_on_previous_table"
    inputs["axis"] = 0
    input_dict["sum_by_column"] = inputs

    TODAY = str(dt.datetime.today()).split(" ")[0]
    configs = {}
    configs["report_title"] = REPORT_TITLE
    configs["export_file_name"] = f"{TODAY}_{file_name}_post_aug01"
    configs["input_dict"] = input_dict

    # df_filter = {}
    # df_filter['col']
    return configs


def sales_by_category_report_configs():
    """
    report type: orders
    """
    REPORT_TITLE = "ORDERS SUBTOTAL EX TAX BY CATEGORY AND BRAND"
    file_name = REPORT_TITLE.lower().replace(" ", "_")

    input_dict = {}

    inputs = {}
    inputs["type"] = "pivot_table"
    inputs["values"] = ["subtotal_ex_tax"]
    inputs["index"] = ["date_created_month", "brand_name"]
    inputs["columns"] = ["category_top"]
    input_dict["ytd_pivot_by_brand_and_categories"] = inputs

    inputs = {}
    inputs["type"] = "pivot_table"
    inputs["values"] = ["subtotal_ex_tax"]
    inputs["index"] = ["category_top", "category_all"]
    inputs["columns"] = ["date_created_month"]
    input_dict["ytd_pivot_by_categories"] = inputs

    inputs = {}
    inputs["type"] = "date_filter"
    inputs["date"] = REPORT_START_DATE
    inputs["column"] = "date_created"
    inputs["bool_op"] = gt
    input_dict["table_modification"] = inputs

    inputs = {}
    inputs["type"] = "pivot_table"
    inputs["values"] = ["subtotal_ex_tax"]
    inputs["index"] = ["date_created_month", "date_created_date"]
    inputs["columns"] = ["brand_name"]
    input_dict["pivot_by_brand_and_date"] = inputs

    inputs = {}
    inputs["type"] = "pivot_table"
    inputs["values"] = ["subtotal_ex_tax"]
    inputs["index"] = ["category_top", "category_all"]
    inputs["columns"] = ["brand_name"]
    input_dict["pivot_by_brand_and_categories"] = inputs

    inputs = {}
    inputs["type"] = "sum_on_previous_table"
    inputs["axis"] = 1
    input_dict["sum_by_row"] = inputs

    inputs = {}
    inputs["type"] = "sum_on_previous_table"
    inputs["axis"] = 0
    input_dict["sum_by_column"] = inputs

    TODAY = str(dt.datetime.today()).split(" ")[0]
    configs = {}
    configs["report_title"] = REPORT_TITLE
    configs["export_file_name"] = f"{TODAY}_{file_name}_post_aug01"
    configs["input_dict"] = input_dict
    return configs


def inventory_valuation_report_configs():
    """
    report type: product
    """
    REPORT_TITLE = "INVENTORY VALUATION REPORT"

    input_dict = {}

    inputs = {}
    inputs["type"] = "groupby_table"
    inputs["values"] = ["price", "cost_price", "inventory_level", "inventory_value", "inventory_value_by_cost"]
    inputs["index"] = ["category_top"]
    inputs["aggfuncs"] = ["sum", "mean"]
    input_dict["groupby_category"] = inputs

    inputs = {}
    inputs["type"] = "groupby_table"
    inputs["values"] = ["price", "cost_price", "inventory_level", "inventory_value", "inventory_value_by_cost"]
    inputs["index"] = ["category_top"]
    inputs["aggfuncs"] = ["sum", "mean", "median", "count"]
    input_dict["groupby_category"] = inputs

    inputs = {}
    inputs["type"] = "groupby_table"
    inputs["values"] = ["price", "cost_price", "inventory_level", "inventory_value", "inventory_value_by_cost"]
    inputs["index"] = ["brand_name"]
    inputs["aggfuncs"] = "sum"
    input_dict["groupby_brand"] = inputs

    inputs = {}
    inputs["type"] = "groupby_table"
    inputs["values"] = ["price", "cost_price", "inventory_level", "inventory_value", "inventory_value_by_cost"]
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

    TODAY = str(dt.datetime.today()).split(" ")[0]
    configs = {}
    configs["report_title"] = REPORT_TITLE
    configs["export_file_name"] = f"{TODAY}_inventory_valuation"
    configs["input_dict"] = input_dict
    return configs
