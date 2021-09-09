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

    def get_product_details(self, order_id: str) -> dict:
        url = f"https://api.bigcommerce.com/stores/yt68tfv9/v2/orders/{order_id}/products"
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


class BigCommProductsAPI(object):
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
        self.url = "/stores/" + self.store_hash + "/v3/catalog/{endpoint}{attribute}"
        self.conn = http.client.HTTPSConnection("api.bigcommerce.com")

    def convert_pages_to_df(self, data):
        """very descriptive docstring"""
        # self.logger.info("converting paginated json to dataframe")
        dfs = []
        for page in data:
            df = pd.DataFrame(data[page]["data"])
            dfs.append(df)
        df = pd.concat(dfs)
        df.reset_index(drop=True, inplace=True)
        return df

    def get_all(self) -> pd.DataFrame:
        """very descriptive docstring"""
        # self.logger.info("get all products in catalog")
        data = {}
        flag = True
        page_num = 0
        endpoint = "products"
        url = self.url.format(endpoint=endpoint, attribute="/?limit=250&page={}")

        while flag:
            page_num += 1
            self.conn.request("GET", url.format(page_num), headers=self.headers)
            res = self.conn.getresponse().read()
            try:
                json_data = json.loads(res.decode("utf-8"))
            except JSONDecodeError as e:
                print(e)

            data[page_num] = json_data
            if page_num % 10 == 0:
                print(
                    "retrieving page "
                    + str(json_data["meta"]["pagination"]["current_page"])
                    + " of "
                    + str(json_data["meta"]["pagination"]["total_pages"])
                )
            if json_data["meta"]["pagination"]["current_page"] == json_data["meta"]["pagination"]["total_pages"]:
                flag = False

        try:
            df = self.convert_pages_to_df(data)
        except:
            pass
            print('pages dictionary unable to convert to dataframe, call "data" attribute')
        return df

    def get_all(self) -> pd.DataFrame:
        """very descriptive docstring"""
        # self.logger.info("get all products in catalog")
        data = {}
        flag = True
        page_num = 0
        endpoint = "products"
        url = self.url.format(endpoint=endpoint, attribute="/?limit=250&page={}")

        while flag:
            page_num += 1
            self.conn.request("GET", url.format(page_num), headers=self.headers)
            res = self.conn.getresponse().read()
            try:
                json_data = json.loads(res.decode("utf-8"))
            except JSONDecodeError as e:
                print(e)

            data[page_num] = json_data
            if page_num % 10 == 0:
                print(
                    f'retrieving page {str(json_data["meta"]["pagination"]["current_page"])} of {str(json_data["meta"]["pagination"]["total_pages"])}'
                )
            if json_data["meta"]["pagination"]["current_page"] == json_data["meta"]["pagination"]["total_pages"]:
                flag = False

        try:
            df = self.convert_pages_to_df(data)
        except:
            pass
            print('pages dictionary unable to convert to dataframe, call "data" attribute')
        return df

    def get_brands(self) -> pd.DataFrame:
        """very descriptive docstring"""
        # self.logger.info("get all products in catalog")
        data = {}
        flag = True
        page_num = 0
        endpoint = "brands"
        url = self.url.format(endpoint=endpoint, attribute="/?limit=250&page={}")

        while flag:
            page_num += 1
            self.conn.request("GET", url.format(page_num), headers=self.headers)
            res = self.conn.getresponse().read()
            try:
                json_data = json.loads(res.decode("utf-8"))
            except JSONDecodeError as e:
                print(e)

            data[page_num] = json_data
            if page_num % 10 == 0:
                print(
                    "retrieving page "
                    + str(json_data["meta"]["pagination"]["current_page"])
                    + " of "
                    + str(json_data["meta"]["pagination"]["total_pages"])
                )
            if json_data["meta"]["pagination"]["current_page"] == json_data["meta"]["pagination"]["total_pages"]:
                flag = False

        try:
            df = self.convert_pages_to_df(data)
        except:
            pass
            print('pages dictionary unable to convert to dataframe, call "data" attribute')
        return df