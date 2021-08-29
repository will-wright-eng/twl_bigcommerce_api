'''general file for utils'''

import configparser
import yaml


def load_yml_configs(file_name:str) -> dict:
    with open(file_name, 'r') as stream:
        try:
            configs = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return configs

def load_config_file(config_part: str) -> dict:
    config = configparser.ConfigParser()
    config.read("project.cfg")
    configs = dict(config.items(config_part))
    return configs