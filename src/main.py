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

from modules.bc_api_orders import BigCommOrdersAPI

from utils.general import export_to_excel, clean_orders
from reports.orders_reports import sales_tax_report_configs, generate_pivot_report


# get data
bco_api = BigCommOrdersAPI()
tmp = bco_api.get_all()

dfs = []
for ind, data in tmp.items():
    dfs.append(pd.DataFrame(data))
    
df = pd.concat(dfs,axis=0)

# generate reports
configs = sales_tax_report_configs()
report, attributes = generate_pivot_report(df=clean_orders(df), configs=configs)

# export
export_to_excel(report['tables'], report['attributes']['export_file_name'])



# project_name = "test"
# base = BigCommProductAPI(project_name)
# df = base.get_all_prods()

# if __name__ == "__main__":
#     main()

###

# order_id = "1455897"
# bco_api.get_order_details(order_id)


# ###

# from bc_api_product import BigCommProductAPI

# base = BigCommProductAPI()
# df = base.get_all_prods()

# df
