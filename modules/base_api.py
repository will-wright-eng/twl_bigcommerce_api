'''docstring'''

import http.client
import json
import logging
import inspect
import configparser


class base_api(object):
    def __init__(self, project_name):
        self.logger = logging.getLogger(project_name)
        config = configparser.ConfigParser()
        config.read('project.cfg')
        configs = dict(config.items('bc_api_creds'))
        self.store_hash = configs['store_hash']
        self.auth_token = configs['x_auth_token']
        self.conn = http.client.HTTPSConnection("api.bigcommerce.com")
        self.headers = {
            'accept': "application/json",
            'content-type': "application/json",
            'x-auth-token': self.auth_token
        }
        self.url = "/stores/" + self.store_hash + "/v3/catalog/{endpoint}{_id}"

    def get_prod(self, _id='8485'):
        self.logger.info('get product: ' + _id)
        endpoint = 'products'
        url = self.url.format(endpoint=endpoint, _id='/' + _id)
        self.conn.request("GET", url, headers=headers)
        res = self.conn.getresponse().read()
        json_data = json.loads(res.decode("utf-8"))
        return json_data

    def get_all_prods(self):
        self.logger.info('get all products in catalog')
        data = {}
        flag = True
        page_num = 0
        endpoint = 'products'
        url = self.url.format(endpoint=endpoint, _id="/?limit=250&page={}")
        while flag:
            page_num += 1
            self.conn.request("GET",
                              url.format(page_num),
                              headers=self.headers)
            res = self.conn.getresponse().read()
            try:
                json_data = json.loads(res.decode("utf-8"))
            except JSONDecodeError as e:
                self.logger.info(e)
                self.logger.info(res)
            data[page_num] = json_data
            self.logger.info(
                str(json_data['meta']['pagination']['current_page']) +
                '\tof\t' + str(json_data['meta']['pagination']['total_pages']))
            if json_data['meta']['pagination']['current_page'] == json_data[
                    'meta']['pagination']['total_pages']:
                self.logger.info(str(flag))
                flag = False
        return data
