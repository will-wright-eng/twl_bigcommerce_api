"""
## (1) MONTHLY REPORT OF SALES FOR SALES TAX PURPOSES BY PAYMENT METHOD
- using [BigCommerce Orders v2 API](https://developer.bigcommerce.com/api-reference/store-management/orders/orders/getallorders) in BigCommOrdersAPI class

## (3) NEED A MONTHLY SALES REPORT BY CATEGORY or BY ITEM.
- using [BigCommerce Orders v2 API](https://developer.bigcommerce.com/api-reference/store-management/orders/orders/getallorders) in BigCommOrdersAPI class
"""

import numpy as np
import pandas as pd


## API JSON standard
# top level
output_response = {}
data = []  # list of reports
meta = {}  # reports generated, sheets in each, and the table shapes

# level 1
report = {}
report["id"] = 1
report["type"] = "twl orders report"
report["attributes"] = {"title": REPORT_TITLE, "input_settings": input_dict}
report["tables"] = {}  # {'table1': pd.DataFrame, 'table2': pd.DataFrame, ...}

## report inputs
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

## generate report
outputs = {}
for table_name, inputs in input_dict.items():
    table = pd.pivot_table(
        df, values=inputs["values"], index=inputs["index"], columns=inputs["columns"], aggfunc=np.sum
    )
    table.columns = [j for i, j in list(table.columns)]
    outputs[table_name] = table

## suppliemental tables
tmp = pd.DataFrame(table.sum(axis=1))
tmp.columns = ["sum"]
outputs["sum_by_month"] = tmp

tmp = pd.DataFrame(table.sum(axis=0))
tmp.columns = ["sum"]
outputs["sum_by_payment_method"] = tmp

outputs["raw_data"] = df

## meta dict
attributes = {}
attributes["report_title"] = REPORT_TITLE
tmp = {"table " + str(i): j for i, j in zip(range(len(list(outputs))), list(outputs))}
attributes.update(tmp)
attributes
