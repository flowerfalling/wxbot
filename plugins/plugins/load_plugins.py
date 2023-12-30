# -*- coding: utf-8 -*-
# @Time    : 2023/12/27 20:40
# @Author  : 之落花--falling_flowers
# @File    : load_plugins.py
# @Software: PyCharm
from types import ModuleType

from Configuration import config
from suswx.common import logger

__all__ = ["load"]


def import_plugin(plugin_path: str) -> None:
    try:
        path: list[str] = plugin_path.split('.')
        m: ModuleType = getattr(__import__('.'.join(path[:-1]), fromlist=path[-1:]), path[-1])
        if "__path__" in dir(m):
            if hasattr(m, "__all__"):
                for i in m.__all__:
                    import_plugin(f"{plugin_path}.{i}")
            else:
                logger.warning(f"The package {plugin_path} has no __all__ attribute.")
    except (ImportError, AttributeError):
        logger.warning(f"Unable to find plugin {plugin_path}.")
        return


def load():
    for plugin in config["plugins"]["list"]:
        import_plugin(f"plugins.{plugin}")
