# -*- coding: utf-8 -*-
# @Time    : 2023/12/15 10:21
# @Author  : 之落花--falling_flowers
# @File    : Configuration.py
# @Software: PyCharm
import yaml


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
        with open(self.config_path) as f:
            self.config = yaml.safe_load(f)

    def save_config(self) -> None:
        """
        Save configuration to config file
        """
        with open(self.config_path, "w+") as f:
            yaml.dump(self.config, f)

    def __getattr__(self, item: str) -> dict:
        """
        Get configuration information from self.config
        :param item: a key of configuration
        :return: the value of self.config
        """
        if item in self.config:
            return self.config[item]
        super().__getattribute__(item)
