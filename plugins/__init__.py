# -*- coding: utf-8 -*-
# @Time    : 2023/12/25 22:26
# @Author  : 之落花--falling_flowers
# @File    : __init__.py.py
# @Software: PyCharm
from Configuration import config
from suswx import logger


def import_plugin(plugin_path: str) -> None:
    try:
        path: list[str] = plugin_path.split('.')
        if len(path) == 1:
            m = __import__(plugin_path)
        else:
            m = getattr(__import__('.'.join(path[:-1]), fromlist=path[-1:]), path[-1])
        if "__path__" in dir(m):
            if getattr(m, "__all__", None) is None:
                logger.warning(f"The package {plugin_path} has no __all__ attribute.")
                return
            for i in m.__all__:
                import_plugin(f"{plugin_path}.{i}")
    except (ImportError, AttributeError):
        logger.warning(f"Unable to find plugin {plugin_path}.")
        return


for plugin in config["plugins"]["list"]:
    import_plugin(plugin)
