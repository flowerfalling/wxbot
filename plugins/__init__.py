# -*- coding: utf-8 -*-
# @Time    : 2023/12/25 22:26
# @Author  : 之落花--falling_flowers
# @File    : __init__.py.py
# @Software: PyCharm
from Configuration import config
from plugins.plugins.utils import load, register, plugins_registry, save_func_config
from schema import Schema

__all__ = ["load", "register", "plugins_registry", "save_func_config"]

plugins_schma = Schema({"info": dict, "list": list})


def init_plugins_config():
    config.config["plugins"] = {"info": {}, "list": []}
    config.save_config()


if not config["plugins"] or not plugins_schma.is_valid(config.config["plugins"]):
    init_plugins_config()
