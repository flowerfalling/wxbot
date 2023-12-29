# -*- coding: utf-8 -*-
# @Time    : 2023/12/12 21:43
# @Author  : 之落花--falling_flowers
# @File    : Robot.py
# @Software: PyCharm
import atexit
import logging
import queue
import time
from threading import Thread
from typing import Callable, Literal, Optional

import wcferry
from wcferry import Wcf, WxMsg

from suswx import Content, ProcessMsgFunc

__all__ = ["robot", "wcf", "logger", "register_func", "register_command", "register_"]

wcf: Wcf = wcferry.Wcf()
logger: logging.Logger = logging.getLogger()
MsgType = Literal[1, 3, 37, 47, 1090519089]
msgtypes: tuple[MsgType, ...] = (1, 3, 37, 47, 1090519089)
func_registry: dict[MsgType, tuple[set, set]] = {i: (set(), set()) for i in msgtypes}
command_registry: dict[int, set] = {i: set() for i in msgtypes}
registry_: list[ProcessMsgFunc] = []
start_mode = Literal["mt", "async"]


def register_(
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


def register_func(
        msgType: tuple[Content],
        fromFriend: bool = False,
        fromGroup: bool = False,
) -> Callable[[Callable[[WxMsg], None]], None]:
    def inner(func: Callable) -> None:
        for i in msgType:
            if fromFriend:
                func_registry[i.value][0].add(func)
            if fromGroup:
                func_registry[i.value][1].add(func)

    return inner


def register_command(
        msgType: tuple[Content],
) -> Callable[[Callable[[WxMsg], None]], None]:
    def inner(func: Callable[[WxMsg], None]) -> None:
        for i in msgType:
            command_registry[i.value].add(func)

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
                self.process_(msg)
            except queue.Empty:
                continue

    def process_(self, msg: WxMsg) -> None:
        if not msg.from_group() and msg.is_text():
            logger.info("[%s]: %s", wcf.get_info_by_wxid(msg.sender)["name"], msg.content)
        for func in registry_:
            if func.check(msg, self.admin):
                func.process(msg)

    def process(self, msg: WxMsg) -> None:
        """
        Group and process information
        :param msg: WxMsg to process
        """
        pass
        from_group: bool = msg.from_group()
        # from_admin: bool = msg.sender == self.admin
        # from_friend: bool = not (from_admin or from_group)
        # msg_type: str = msg.type
        if not from_group and msg.is_text():
            logger.info("[%s]: %s", wcf.get_info_by_wxid(msg.sender)["name"], msg.content)
        # if from_admin:
        #     if msg.content == "/quit":
        #         exit(0)
        #     func: set[Callable] = command_registry[msg.type]
        # elif func_registry.get(msg.type) is not None:
        #     func: set[Callable] = func_registry[msg.type][from_group]
        # else:
        #     return
        # if func:
        #     for i in func:
        #         Thread(target=i, args=(msg,)).start()


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
