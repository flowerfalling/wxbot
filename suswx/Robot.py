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

__all__ = ["robot", "wcf"]

wcf: Wcf = wcferry.Wcf()


class Robot(object):
    """
    A WeChat robot framework
    """

    def __init__(self, logger: logging.Logger, admin: str = None) -> None:
        self.wcf: Wcf = wcf
        self.admin: str = wcf.get_self_wxid()
        if admin := list(filter(lambda x: x['name'] == admin, wcf.get_friends())):
            self.admin = admin[0]['wxid']
        self.registry: dict = {
            i: ([], []) for i in (1, 3, 37, 47, 1090519089)
        }  # (私聊, 组群)
        self.command: dict = {
            i: [] for i in (1, 3, 37, 47, 1090519089)
        }
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
            func: list[Callable] = self.command[msg.type]
        elif self.registry.get(msg.type) is not None:
            func: list[Callable] = self.registry[msg.type][from_group]
        else:
            return
        if func:
            for i in func:
                Thread(target=i, args=(msg,)).start()

    def register(
            self,
            func: Callable[[WxMsg], None],
            msgType: tuple[Content],
            fromGroup: bool = False,
            fromFriend: bool = False,
    ) -> None:
        """
        Register a processing method with the robot to process other's messages
        :param func: a callable to register
        :param msgType: the msg type list to process
        :param fromGroup: allow to process group messages
        :param fromFriend: allow to process friend messages
        """
        for i in msgType:
            if fromFriend:
                self.registry[i.value][0].append(func)
            if fromGroup:
                self.registry[i.value][1].append(func)

    def register_command(self, func: Callable[[wcferry.WxMsg], None], msgType: tuple[Content]) -> None:
        """
        Register a processing method with the robot to process the administrator's command
        :param func: a callable to register
        :param msgType: the msg type list to register
        """
        for i in msgType:
            self.command[i.value].append(func)


def robot(name: str = "SUSBOT", debug: bool = True, admin: str = None) -> tuple[Robot, wcferry.Wcf, logging.Logger, str]:
    """
    Get a WeChat bot
    :param name: the bot's name
    :param debug: whether to enable debugging
    :param admin: the administrator's wxid
    :return: robot instance, wcferry instance, logger instance, admin's wxid
    """
    wcf: wcferry.Wcf = wcferry.Wcf(debug=debug)
    logger: logging.Logger = logging.getLogger(name)
    bot: Robot = Robot(wcf, logger, admin)
    atexit.register(wcf.cleanup)
    atexit.register(lambda: print("Quit done"))
    return bot, wcf, logger, bot.admin
