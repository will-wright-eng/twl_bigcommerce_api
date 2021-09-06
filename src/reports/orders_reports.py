"""
## (1) MONTHLY REPORT OF SALES FOR SALES TAX PURPOSES BY PAYMENT METHOD
- using [BigCommerce Orders v2 API](https://developer.bigcommerce.com/api-reference/store-management/orders/orders/getallorders) in BigCommOrdersAPI class

## (3) NEED A MONTHLY SALES REPORT BY CATEGORY AND BY ITEM.
- using [BigCommerce Orders v2 API](https://developer.bigcommerce.com/api-reference/store-management/orders/orders/getallorders) in BigCommOrdersAPI class
"""


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


