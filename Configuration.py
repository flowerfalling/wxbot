# -*- coding: utf-8 -*-
# @Time    : 2023/12/15 10:21
# @Author  : 之落花--falling_flowers
# @File    : Configuration.py
# @Software: PyCharm
import os

import yaml

__all__ = ["config"]


class Configuration(object):
    """
    To load and save configuration

    Do not write keys whose names are object's attributes or method names in the configuration file.
    """

    def __init__(self, config_path="./config.yaml") -> None:
        """
        :param config_path: config file path
        """
        self.config_path: str = config_path
        self.config: dict = {}
        self.load_config()

    def load_config(self) -> None:
        """
        Load configuration by config file
        """
        if not os.path.exists(self.config_path):
            open(self.config_path, "w+").close()
        with open(self.config_path, encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

    def save_config(self) -> None:
        """
        Save configuration to config file
        """
        with open(self.config_path, "w+", encoding='utf-8') as f:
            yaml.dump(self.config, f, allow_unicode=True)
        self.load_config()

    def __getitem__(self, key: str) -> object:
        if key in self.config:
            return self.config[key]
        return None


config: Configuration = Configuration()

