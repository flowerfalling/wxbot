# -*- coding: utf-8 -*-
# @Time    : 2023/12/12 21:43
# @Author  : 之落花--falling_flowers
# @File    : Robot.py
# @Software: PyCharm
import atexit
import queue
import time
from typing import Callable

import wcferry
from wcferry import Wcf

from suswx.Content import Content


class Robot(object):
    def __init__(self, wcf: Wcf) -> None:
        self.wcf = wcf
        self.registry: dict = dict.fromkeys((0, 1, 3, 37, 47, 1090519089), ([], []))  # (私聊, 组群)

    def run(self) -> None:
        self.wcf.enable_receiving_msg()
        while self.wcf.is_receiving_msg():
            time.sleep(0.5)
            try:
                msg = self.wcf.get_msg()
                if msg.from_self() and msg.content == "/quit":
                    break
                self.process(msg)
            except queue.Empty:
                continue

    def process(self, msg: wcferry.WxMsg) -> None:
        from_group = int(msg.from_group())
        if msg.from_self():
            func = self.registry[0][from_group]
        else:
            func = self.registry.get(msg.type)[from_group]
        if func:
            for i in func:
                i(msg)

    def register(
            self,
            func: Callable,
            msgType: Content,
            fromGroup: bool = False,
            fromFriend: bool = False,
    ) -> None:
        if fromFriend:
            self.registry[msgType.value][0].append(func)
        if fromGroup:
            self.registry[msgType.value][1].append(func)

    def register_command(self, func: Callable) -> None:
        self.registry["me"].append(func)

    @atexit.register
    def quit(self) -> None:
        self.wcf.cleanup()
        print('Quit done')
