# -*- coding: utf-8 -*-
# @Time    : 2023/12/12 21:43
# @Author  : 之落花--falling_flowers
# @File    : Robot.py
# @Software: PyCharm
import queue
import time
from enum import Enum
from typing import Callable

import wcferry
from wcferry import Wcf
from GPT import GPT


class Robot(object):
    def __init__(self, wcf: Wcf) -> None:
        self.wcf = wcf
        self.registry: dict = dict.fromkeys((0, 1, 3, 37, 47, 1090519089), ([], []))  # (私聊, 组群)

    def run(self) -> None:
        while self.wcf.enable_receiving_msg():
            time.sleep(0.5)
            try:
                msg = self.wcf.get_msg()
                if msg.from_self() and msg.content == "/quit":
                    break
                try:
                    self.process(msg)
                except:
                    break
                self.process(msg)
            except queue.Empty:
                continue
        self.quit()

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
            msgType: "Robot.Content",
            fromGroup: bool = False,
            fromFriend: bool = False,
    ) -> None:
        if fromFriend:
            self.registry[msgType.value][0].append(func)
        if fromGroup:
            self.registry[msgType.value][1].append(func)

    def register_command(self, func: Callable) -> None:
        self.registry["me"].append(func)

    def quit(self) -> None:
        self.wcf.cleanup()

    class Content(Enum):
        TEXT = 1
        PICTURE = 3
        AUDIO = 34
        VIDEO = 47
        FILE = 1090519089


def main():
    wcf = Wcf(debug=True)
    robot = Robot(wcf)
    robot.register(GPT(wcf).private_reply, Robot.Content.TEXT, False, True)
    robot.run()


if __name__ == "__main__":
    main()
