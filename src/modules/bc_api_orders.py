"""docstring"""

import yaml
import json
import logging
import inspect
import http.client

import pandas as pd

from json import JSONDecodeError

from utils.general import load_yml_configs


class BigCommOrdersAPI(object):
    """very descriptive docstring"""

    def __init__(self, project_name=None):
        configs = load_yml_configs("configs.yml")["bigcomm_creds"]["bc_api_read-only"]
        self.store_hash = configs["store_hash"]
        self.auth_token = configs["x_auth_token"]
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-auth-token": self.auth_token,
        }
        self.url = "/stores/" + self.store_hash + "/v2/{endpoint}{attribute}"
        self.conn = http.client.HTTPSConnection("api.bigcommerce.com")

    def get_order_details(self, order_id: str) -> dict:
        url = (
            f"https://api.bigcommerce.com/stores/yt68tfv9/v2/orders/{order_id}/products"
        )
        self.conn.request("GET", url, headers=self.headers)
        res = self.conn.getresponse().read()
        try:
            json_data = json.loads(res.decode("utf-8"))
        except JSONDecodeError as e:
            print("error:" + e)
        return json_data

    def get_all(self, min_date_modified: str = "2021-08-01") -> dict:
        """very descriptive docstring"""
        data = {}
        flag = True
        page_num = 0
        endpoint = "orders"
        url = self.url.format(
            endpoint=endpoint,
            attribute="/?limit=250&page={}" + f"&min_date_modified={min_date_modified}",
        )
        while flag:
            page_num += 1
            self.conn.request("GET", url.format(page_num), headers=self.headers)

            res = self.conn.getresponse().read()
            try:
                json_data = json.loads(res.decode("utf-8"))
            except JSONDecodeError as e:
                print("error:" + e)
                return json_data, flag, res
            data[page_num] = json_data
            if page_num > 1 and len(json_data) < 250:
                flag = False
        return data
