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

    def __init__(self, admin: str = None) -> None:
        self.config = config
        self.sus = robot(name=self.config["logger"]["name"], admin=admin)

    def run(self) -> None:
        """
        Start the robot
        """
        self.sus.run()


def main() -> None:
    susbot = SusRobot(admin="\u3000\u3000")
    susbot.run()


if __name__ == "__main__":
    main()
