"""docstring"""

import yaml
import json
import logging
import inspect
import http.client
import configparser

import pandas as pd

from json import JSONDecodeError

from utils.general import load_yml_configs


class BigCommProductAPI(object):
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

    def get_prod(self, _id="8485"):
        """very descriptive docstring"""
        self.logger.info("get product: " + str(_id))
        endpoint = "products"
        url = self.url.format(endpoint=endpoint, attribute="/" + str(_id))
        self.conn.request("GET", url, headers=self.headers)
        res = self.conn.getresponse()
        if res.code == 200:
            self.logger.info("response code: " + str(res.code))
        else:
            self.logger.warning("response code: " + str(res.code) + " product id " + str(_id) + " unsuccessful")
        json_data = json.loads(res.read().decode("utf-8"))
        return json_data["data"]

    def convert_pages_to_df(self, data):
        """very descriptive docstring"""
        self.logger.info("converting paginated json to dataframe")
        dfs = []
        for page in data:
            df = pd.DataFrame(data[page]["data"])
            dfs.append(df)
        df = pd.concat(dfs)
        df.reset_index(drop=True, inplace=True)
        return df

    def get_all_prods(self):
        """very descriptive docstring"""
        self.logger.info("get all products in catalog")
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
                self.logger.warning(e)
                self.logger.info(res)
            data[page_num] = json_data
            if page_num % 10 == 0:
                self.logger.info(
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
            self.logger.error('pages dictionary unable to convert to dataframe, call "data" attribute')
        return df

    def put_prod_desc(self, new_html, _id="8485"):
        """very descriptive docstring"""
        self.logger.info("modify product description: " + str(_id))
        payload = json.dumps({"description": new_html})
        url = self.url.format(endpoint="products", attribute="/" + str(_id))
        self.conn.request("PUT", url, payload, headers=self.headers)
        res = self.conn.getresponse()
        if res.code == 200:
            self.logger.info("response code: " + str(res.code))
        else:
            self.logger.warning("response code: " + str(res.code) + " product id " + str(_id) + " unsuccessful")
