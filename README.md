# TWL Reports
Programatically extracting data from BigCommerce for custom reports

## Table of Contents
- [Reports Summary](#reports-summary)
- [Notes](#notes)
- [Repo Tree](#repo-tree)
- [TODO](#todo)

## Usage Notes
- `conda create -n twl python=3.8`
- `conda activate twl`
- `pip install -r requirements.txt`

## Reports Summary
### (1) MONTHLY REPORT OF SALES FOR SALES TAX PURPOSES BY PAYMENT METHOD
- using [BigCommerce Orders v2 API](https://developer.bigcommerce.com/api-reference/store-management/orders/orders/getallorders) in BigCommOrdersAPI class

### (2) MONTHLY REPORTS FOR INVENTORY VALUATION
- using [BigCommerce Catalog/Products v3 API](https://developer.bigcommerce.com/api-reference/store-management/catalog/products/getproducts) in BigCommProductsAPI class

### (3) NEED A MONTHLY SALES REPORT BY CATEGORY or BY ITEM.
- using [BigCommerce Orders v2 API](https://developer.bigcommerce.com/api-reference/store-management/orders/orders/getallorders) in BigCommOrdersAPI class

Reports Breakout
[data source | report | data view / pivot table]
![reports_lineage](.images/reports_lineage.png)

## Notes
```
main.py docstring

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

```

## Repo Tree
```bash
% tree --filelimit 9
.
├── LICENSE
├── README.md
├── images
│   └── reports_lineage.png
├── requirements.txt
└── src
    ├── __init__.py
    ├── configs.yml
    ├── main.py
    ├── modules
    │   ├── __init__.py
    │   └── bigcomm_api.py
    ├── reports
    │   ├── __init__.py
    │   ├── orders_reports.py
    │   └── product_reports.py
    └── utils
        └── general.py
```

## TODO
- email module
- abstract out report parameters
- add concurrency/multithreading/asyncio
    - https://www.integralist.co.uk/posts/python-asyncio/
    - https://pymotw.com/3/concurrency.html
    - [pluralsight course](https://www.pluralsight.com/courses/python-concurrency-getting-started?aid=701j0000001heIoAAI&promo=&utm_source=non_branded&utm_medium=digital_paid_search_google&utm_campaign=US_Dynamic&utm_content=&cq_cmp=175953558&gclid=CjwKCAjwndCKBhAkEiwAgSDKQWeoq-az9nEmDHwyaBrCNq-_myyUTN2WnF2rNdP5OhL8hCMMO4SXQRoC4j0QAvD_BwE#)
- allow reports to be run on backup file (modify get_data arguement "source" to default to api, but S3 file can be specified)