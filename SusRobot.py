# -*- coding: utf-8 -*-
# @Time    : 2023/12/15 9:47
# @Author  : 之落花--falling_flowers
# @File    : SusRobot.py
# @Software: PyCharm
import logging

from wcferry import Wcf

from funcs import funcs
from funcs.Command import gpt
from funcs.GPT import GPT
from suswx import Robot, Content, Configuration

logging.basicConfig(
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO,
)


class SusRobot:
    """
    A WeChat Robot demo
    """

    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger("SUSBOT")
        self.wcf: Wcf = Wcf(debug=True)
        self.sus: Robot = Robot(self.wcf, self.logger)
        self.config: Configuration = Configuration("./config.yaml")
        self.sus.register(
            GPT(self.wcf, self.config).private_reply, (Content.TEXT,), fromFriend=True
        )
        self.sus.register(
            funcs.hitokoto(self.wcf, self.config), (Content.TEXT.TEXT,), fromFriend=True
        )
        self.sus.register_command(gpt(self.wcf, self.config, self.logger))

    def run(self) -> None:
        """
        Start the robot
        """
        self.sus.run()


def main() -> None:
    susbot = SusRobot()
    susbot.run()


if __name__ == "__main__":
    main()
