# -*- coding: utf-8 -*-
# @Time    : 2023/12/15 9:47
# @Author  : 之落花--falling_flowers
# @File    : SusRobot.py
# @Software: PyCharm
import logging

import plugins
from suswx.bot import robot

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
        self.sus = robot()
        plugins.load()


def main() -> None:
    susbot: SusRobot = SusRobot()
    susbot.sus.run()


if __name__ == "__main__":
    main()
