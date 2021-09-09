"""
## (1) MONTHLY REPORT OF SALES FOR SALES TAX PURPOSES BY PAYMENT METHOD
- using [BigCommerce Orders v2 API](https://developer.bigcommerce.com/api-reference/store-management/orders/orders/getallorders) in BigCommOrdersAPI class


## (2) MONTHLY REPORTS FOR INVENTORY VALUATION
- using [BigCommerce Catalog/Products v3 API](https://developer.bigcommerce.com/api-reference/store-management/catalog/products/getproducts) in BigCommProductsAPI class


## (3) NEED A MONTHLY SALES REPORT BY CATEGORY AND BY ITEM.
- using [BigCommerce Orders v2 API](https://developer.bigcommerce.com/api-reference/store-management/orders/orders/getallorders) in BigCommOrdersAPI class
"""


import datetime as dt


def sales_tax_report_configs():
    """
    report type: orders
    """
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

    # df_filter = {}
    # df_filter['col']
    return configs


def sales_by_category_report_configs():
    """
    report type: orders
    """
    REPORT_TITLE = "SALES REPORT BY CATEGORY AND BY ITEM"

    input_dict = {}

    inputs = {}
    inputs["values"] = ["subtotal_ex_tax"]
    inputs["index"] = ["date_created_month", "brand_name"]
    inputs["columns"] = ["category_top"]
    input_dict["pivot_by_day"] = inputs

    inputs = {}
    inputs["values"] = ["subtotal_ex_tax", "subtotal_inc_tax", "subtotal_tax"]
    inputs["index"] = ["date_created_month", "brand_name"]
    inputs["columns"] = ["category_top"]
    input_dict["pivot_by_month"] = inputs

    TODAY = str(dt.datetime.today()).split(" ")[0]
    configs = {}
    configs["report_title"] = REPORT_TITLE
    configs["export_file_name"] = f"{TODAY}_sales_by_category_post_aug01"
    configs["input_dict"] = input_dict
    return configs


def inventory_valuation_report_configs():
    """
    report type: product
    """
    REPORT_TITLE = "MONTHLY REPORTS FOR INVENTORY VALUATION"

    input_dict = {}

    inputs = {}
    inputs["values"] = ["price", "cost_price", "retail_price", "sale_price", "map_price", "calculated_price"]
    inputs["index"] = ["brand_name", "category_top", "category_all"]
    inputs["columns"] = ["date_created_month"]
    input_dict["pivot_price_cols"] = inputs

    inputs = {}
    inputs["values"] = ["price"]
    inputs["index"] = ["brand_name", "category_top", "category_all"]
    inputs["columns"] = ["date_created_month"]
    input_dict["pivot_price_cols"] = inputs

    TODAY = str(dt.datetime.today()).split(" ")[0]
    configs = {}
    configs["report_title"] = REPORT_TITLE
    configs["export_file_name"] = f"{TODAY}_inventory_valuation"
    configs["input_dict"] = input_dict
    return configs
