# -*- coding: utf-8 -*-
# @Time    : 2023/12/15 9:47
# @Author  : 之落花--falling_flowers
# @File    : SusRobot.py
# @Software: PyCharm
import logging

from plugins import funcs
from suswx import robot, Content

logging.basicConfig(
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO,
)


class SusRobot:
    """
    A WeChat Robot demo
    """

    def __init__(
            self,
            name: str = "SUSBOT",
            admin: str = None
    ) -> None:
        self.sus = robot(name=name, admin=admin)
        # self.sus.register(
        #     GPT(self.wcf, self.config, self.logger, "GPT", "/").private_reply, (Content.TEXT,), fromFriend=True
        # )
        # self.sus.register(
        #     Gemini(self.wcf, self.config, self.logger, "Gemini", "%").private_reply, (Content.TEXT,), fromFriend=True
        # )
        # self.sus.register(
        #     plugins.hitokoto(self.wcf, self.config, self.logger), (Content.TEXT,), fromFriend=True
        # )
        # self.sus.register(
        #     plugins.menu(self.wcf, self.config, self.logger), (Content.TEXT,), fromFriend=True
        # )
        # self.sus.register_command(Administrator(self.wcf, self.config, self.logger, self.admin), (Content.TEXT,))
        self.sus.register_((Content.TEXT,), True)(funcs.funcs.hitokoto)
        self.sus.register_((Content.TEXT,), True)(funcs.funcs.menu)
        # self.sus.register_((Content.TEXT,), True)(AI.AI.GPT().private_reply)

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
