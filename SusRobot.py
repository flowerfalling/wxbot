# -*- coding: utf-8 -*-
# @Time    : 2023/12/15 9:47
# @Author  : 之落花--falling_flowers
# @File    : SusRobot.py
# @Software: PyCharm
import logging

from Configuration import config
from suswx import robot
import plugins

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
        self.config = config
        self.sus = robot(name=self.config["logger"]["name"])
        plugins.load()

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
