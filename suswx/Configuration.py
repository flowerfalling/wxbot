# -*- coding: utf-8 -*-
# @Time    : 2023/12/15 10:21
# @Author  : 之落花--falling_flowers
# @File    : Configuration.py
# @Software: PyCharm
import yaml


class Configuration(object):
    def __init__(self, config_path='./config.yaml'):
        self.config_path: str = config_path
        self.config: dict = {}
        self.load_config()

    def load_config(self):
        with open(self.config_path) as f:
            self.config = yaml.safe_load(f)

    def save_config(self):
        with open(self.config_path, 'w+') as f:
            yaml.dump(self.config, f)

    def __getattr__(self, item):
        if item in self.config:
            return self.config[item]
        super().__getattribute__(item)
