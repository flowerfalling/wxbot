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
from typing import Callable

import wcferry
from wcferry import Wcf, WxMsg

from suswx import Content

__all__ = ["robot", "wcf", "logger", "register_func", "register_command"]

wcf: Wcf = wcferry.Wcf()
logger: logging.Logger = logging.getLogger()
msgtype: tuple[int, ...] = (1, 3, 37, 47, 1090519089)
func_registry: dict[int, tuple[set, set]] = {i: (set(), set()) for i in msgtype}
command_registry: dict[int, set] = {i: set() for i in msgtype}


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

    def __init__(self, admin: str = None) -> None:
        self.wcf: Wcf = wcf
        self.admin: str = wcf.get_self_wxid()
        if admin := list(filter(lambda x: x['name'] == admin, wcf.get_friends())):
            self.admin = admin[0]['wxid']
        self._registry: dict[int, tuple[set, set]] = func_registry
        self.command: dict[int, set] = command_registry
        self.logger: logging.Logger = logger

    def run(self) -> None:
        """
        Keep the bot running and processing information
        """
        self.wcf.enable_receiving_msg()
        interval: float = 0.5
        while self.wcf.is_receiving_msg():
            time.sleep(interval)
            try:
                msg: WxMsg = self.wcf.get_msg()
                self.process(msg)
            except queue.Empty:
                continue

    def process(self, msg: WxMsg) -> None:
        """
        Group and process information
        :param msg: WxMsg to process
        """
        from_group: int = int(msg.from_group())
        from_self: bool = msg.sender == self.admin
        if not from_group and msg.is_text():
            self.logger.info("[%s]: %s", self.wcf.get_info_by_wxid(msg.sender)["name"], msg.content)
        if from_self:
            if msg.content == "/quit":
                exit(0)
            func: set[Callable] = self.command[msg.type]
        elif self._registry.get(msg.type) is not None:
            func: set[Callable] = self._registry[msg.type][from_group]
        else:
            return
        if func:
            for i in func:
                Thread(target=i, args=(msg,)).start()


def robot(name: str = "SUSBOT", admin: str = None) -> Robot:
    """
    Get a WeChat bot
    :param name: the bot's name
    :param admin: the administrator's wxid
    :return: robot instance, wcferry instance, logger instance, admin's wxid
    """
    logger.name = name
    bot: Robot = Robot(admin)
    atexit.register(wcf.cleanup)
    atexit.register(lambda: print("Quit done"))
    return bot
