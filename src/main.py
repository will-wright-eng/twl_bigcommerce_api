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

"""

# import os
# import http.client
# import json
# import logging
# import inspect
# import configparser
# import datetime as dt

import pandas as pd

# import modules.util_fxns as utilf
from modules.base_api import BigCommProductAPI

project_name = "test"
base = BigCommProductAPI(project_name)
df = base.get_all_prods()

if __name__ == "__main__":
    main()
