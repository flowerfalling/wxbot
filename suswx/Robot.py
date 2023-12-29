# -*- coding: utf-8 -*-
# @Time    : 2023/12/12 21:43
# @Author  : 之落花--falling_flowers
# @File    : Robot.py
# @Software: PyCharm
import atexit
import logging
import queue
import time
from typing import Callable, Literal, Optional

import wcferry
from wcferry import Wcf, WxMsg

from suswx import Content, ProcessMsgFunc

__all__ = ["robot", "wcf", "logger", "register"]

wcf: Wcf = wcferry.Wcf()
logger: logging.Logger = logging.getLogger()
MsgType = Literal[1, 3, 37, 47, 1090519089]
msgtypes: tuple[MsgType, ...] = (1, 3, 37, 47, 1090519089)
func_registry: dict[MsgType, tuple[set, set]] = {i: (set(), set()) for i in msgtypes}
command_registry: dict[int, set] = {i: set() for i in msgtypes}
registry_: list[ProcessMsgFunc] = []
start_mode = Literal["mt", "async"]


def register(
        msgType: tuple[Content] = (Content.TEXT,),
        fromFriend: bool = False,
        fromGroup: bool = False,
        fromAdmin: bool = False,
        name: Optional[str] = None,
        mode: start_mode = "mt",
) -> Callable[[Callable[[WxMsg], None]], None]:
    def inner(func: Callable[[WxMsg], None]) -> None:
        func_name = name if name is not None else func.__name__
        registry_.append(ProcessMsgFunc(func, func_name, msgType, fromFriend, fromGroup, fromAdmin, mode))

    return inner


class Robot(object):
    """
    A WeChat robot framework
    """

    def __init__(self) -> None:
        self.admin: str = wcf.get_self_wxid()
        self.interval: float = 0.5

    def run(self) -> None:
        """
        Keep the bot running and processing information
        """
        wcf.enable_receiving_msg()
        while wcf.is_receiving_msg():
            time.sleep(self.interval)
            try:
                msg: WxMsg = wcf.get_msg()
                self.process(msg)
            except queue.Empty:
                continue

    def process(self, msg: WxMsg) -> None:
        if not msg.from_group() and msg.is_text():
            logger.info("[%s]: %s", wcf.get_info_by_wxid(msg.sender)["name"], msg.content)
        for func in registry_:
            if func.check(msg, self.admin):
                func.process(msg)


def robot(name: str = "SUSBOT") -> Robot:
    """
    Get a WeChat bot
    :param name: the bot's name
    :return: robot instance, wcferry instance, logger instance, admin's wxid
    """
    logger.name = name
    bot: Robot = Robot()
    atexit.register(wcf.cleanup)
    atexit.register(lambda: print("Quit done"))
    return bot
