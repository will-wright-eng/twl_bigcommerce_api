# TWL Reports
Programatically extracting data from BigCommerce for custom reports

Reports Breakout
[data source | report | data view / pivot table]
![reports_lineage](./reports_lineage.png)

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

## Tree

```bash
% tree --filelimit 9
.
├── LICENSE
├── README.md
├── notes
├── reports_lineage.png
└── src
    ├── Untitled.ipynb
    ├── bc_api_orders.py
    ├── bc_api_product.py
    ├── main.py
    └── project.cfg
```