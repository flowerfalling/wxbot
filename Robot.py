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


class Robot(object):
    def __init__(self):
        self.wcf = Wcf(debug=True)

    def run(self):
        while self.wcf.enable_receiving_msg():
            time.sleep(0.5)
            try:
                msg = self.wcf.get_msg()
                self.process(msg)
            except queue.Empty:
                continue

    def process(self, msg: wcferry.WxMsg):
        pass

    def register(
            self, func: Callable, msgType: "Robot.Type", fromGroup: bool = False, fromFriend: bool = False
    ):
        pass

    def register_command(self, func: Callable, msgType: "Robot.Type"):
        pass

    def quit(self):
        self.wcf.cleanup()

    class Type(Enum):
        TEXT = 1
        PICTURE = 2
        VIDEO = 3
        AUDIO = 4
        FILE = 5


def main():
    robot = Robot()
    robot.run()


if __name__ == "__main__":
    main()
