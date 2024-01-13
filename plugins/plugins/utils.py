# -*- coding: utf-8 -*-
# @Time    : 2023/12/27 20:40
# @Author  : 之落花--falling_flowers
# @File    : utils.py
# @Software: PyCharm
from types import ModuleType
from typing import Callable, Literal, Optional

from schema import Schema
from wcferry import WxMsg

from Configuration import config
from suswx import ProcessMsgFunc, Content
from suswx.Registry import func_startup_mode
from suswx.common import logger
import suswx.bot

__all__ = ["load", "register", "plugins_registry"]

plugin_config_schma = Schema({"access": list, "enable": bool})
pfunc_mode = Literal["frozen", "save"]
plugins_registry: dict[pfunc_mode, set[ProcessMsgFunc]] = {"frozen": set(), "save": set()}


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


def register(
        msgType: tuple[Content] = (Content.TEXT,),
        fromFriend: bool = False,
        fromGroup: bool = False,
        fromAdmin: bool = False,
        name: Optional[str] = None,
        mode: func_startup_mode = "mt",
        enable: bool = True,
        access: Optional[set] = None,
        frozen: bool = False,
        save_config: bool = True
) -> Callable[[Callable[[WxMsg], None]], None]:
    # noinspection PyUnresolvedReferences
    """
        This registration method is a wrapper for suswx.bot's registration method, allowing users to create configurations in configuration files or prohibiting administrators from changing the method.
        You can use this function like this:

        >>> @plugins.register(save_config=True)
        >>> def func(msg: wcferry.WxMsg) -> None:
        >>>     ...

        :param msgType: a tuple of Message types allowed to be processed
        :param fromFriend: Whether to handle messages from friends
        :param fromGroup: Whether to handle messages from groups
        :param fromAdmin: Whether to handle messages from the admin
        :param name: Function name (Optional, default is function name)
        :param mode: Function startup method (multithreaded "mt" or asynchronous "async")
        :param enable: Whether to enable
        :param access: The set of wxids of allowed message senders(Optional)
        :param frozen: Whether to freeze this function (cannot be modified)
        :param save_config: Whether to set default configuration, including access and enable, and will be written to config.yaml
        :return: A decorator used to register functions
    """

    def inner(func: Callable[[WxMsg], None]) -> None:
        """
        :param func: A decorator used to register functions
        """
        func_item: ProcessMsgFunc = suswx.bot.register(msgType, fromFriend, fromGroup, fromAdmin, name, mode, enable, access)(func)
        func_name = func_item.name
        if frozen:
            plugins_registry["frozen"].add(func_item)
        else:
            if save_config:
                plugins_registry["save"].add(func_item)
                if config["plugins"]["info"].get(func_name) is None:
                    config["plugins"]["info"][func_name] = {"access": [], "enable": False}
                    config.save_config()
                func_item.access = set(config["plugins"]["info"][func_name]["access"])
                func_item.enable = config["plugins"]["info"][func_name]["enable"]

    return inner
