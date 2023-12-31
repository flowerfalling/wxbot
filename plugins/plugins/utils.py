# -*- coding: utf-8 -*-
# @Time    : 2023/12/27 20:40
# @Author  : 之落花--falling_flowers
# @File    : utils.py
# @Software: PyCharm
from types import ModuleType
from typing import Callable

from schema import Schema

from Configuration import config
from suswx import ProcessMsgFunc
from suswx.common import logger

__all__ = ["load", "init"]

plugin_config_schma = Schema({"access": list, "enable": bool})


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
        else:
            logger.info(f"Successfully loaded function {m.__name__}")
    except (ImportError, AttributeError):
        logger.warning(f"Unable to find plugin {plugin_path}.")
        return


def load():
    for plugin in config["plugins"]["list"]:
        import_plugin(f"plugins.{plugin}")


def init(def_config: bool = True) -> Callable:
    # noinspection PyUnresolvedReferences
    """
        This function is used to check and write the default configuration framework in config for functions that need to be registered into the bot, including access and enable.

        You can use this function like this:

        >>> @plugins.init(def_config=True)
        >>> @suswx.bot.register()
        >>> def func(msg: wcferry.WxMsg) -> None:
        >>>     ...

        :param def_config: Whether to set default configuration, including access and enable, and will be written to config.yaml
    """

    def inner(func_item: ProcessMsgFunc) -> None:
        """
        :param func_item: The ProcessMsgFunc instance
        """
        name = func_item.name
        if def_config:
            if config["plugins"]["info"].get(name) is None:
                config["plugins"]["info"][name] = {"access": [], "enable": False}
                config.save_config()
            func_item.access = set(config["plugins"]["info"][name]["access"])
            func_item.enable = config["plugins"]["info"][name]["enable"]
        else:
            from plugins.Administrator.Administrator import special_func
            special_func.add(func_item.name)

    return inner
