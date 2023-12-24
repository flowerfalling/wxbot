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


class Robot(object):
    """
    A WeChat robot framework
    """

    def __init__(self, wcf: Wcf, logger: logging.Logger) -> None:
        """
        :param wcf: your wcf instance
        """
        self.wcf: Wcf = wcf
        self.registry: dict = {
            i: ([], []) for i in (0, 1, 3, 37, 47, 1090519089)
        }  # (私聊, 组群), 0为自己
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
                if msg.from_self() and msg.content == "/quit":
                    break
                self.process(msg)
            except queue.Empty:
                continue

    def process(self, msg: WxMsg) -> None:
        """
        Group and process information
        :param msg: WxMsg to process
        """
        from_group: int = int(msg.from_group())
        if not from_group and msg.is_text():
            self.logger.info(
                "[%s]: %s",
                self.wcf.get_info_by_wxid(msg.sender)["name"], msg.content,
            )
        if msg.from_self():
            func: list[Callable] = self.registry[0][0]
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

    def register_command(self, func: Callable) -> None:
        """
        Register a processing method with the robot to process the administrator's command
        :param func: a callable to register
        """
        self.registry[0][0].append(func)


def robot(name: str, debug: bool = True) -> tuple[Robot, wcferry.Wcf, logging.Logger]:
    wcf = wcferry.Wcf(debug=debug)
    logger = logging.getLogger(name)
    bot = Robot(wcf, logger)
    atexit.register(wcf.cleanup)
    return bot, wcf, logger
