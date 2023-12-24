# -*- coding: utf-8 -*-
# @Time    : 2023/12/15 10:21
# @Author  : 之落花--falling_flowers
# @File    : Configuration.py
# @Software: PyCharm
import yaml

__all__ = ["Configuration"]


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
        with open(self.config_path, encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

    def save_config(self) -> None:
        """
        Save configuration to config file
        """
        with open(self.config_path, "w+", encoding='utf-8') as f:
            yaml.dump(self.config, f)
        self.load_config()

    def __getitem__(self, item: str) -> dict:
        if item in self.config:
            return self.config[item]
        raise None

