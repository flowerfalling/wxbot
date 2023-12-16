# -*- coding: utf-8 -*-
# @Time    : 2023/12/15 9:47
# @Author  : 之落花--falling_flowers
# @File    : demo.py
# @Software: PyCharm
import logging

from wcferry import Wcf

from Command import gpt
from GPT import GPT
from suswx import Robot, Content, Configuration

logging.basicConfig(
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO,
)


class SusRobot:
    def __init__(self):
        self.logger: logging.Logger = logging.getLogger("SUSBOT")
        self.wcf: Wcf = Wcf(debug=True)
        self.sus: Robot = Robot(self.wcf, self.logger)
        self.config: Configuration = Configuration("./config.yaml")
        self.sus.register(GPT(self.wcf, self.config).private_reply, (Content.TEXT,), fromFriend=True)
        self.sus.register_command(gpt(self.wcf, self.config, self.logger))

    def run(self):
        self.sus.run()


def main():
    susbot = SusRobot()
    susbot.run()


if __name__ == "__main__":
    main()