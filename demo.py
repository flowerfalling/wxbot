# -*- coding: utf-8 -*-
# @Time    : 2023/12/15 9:47
# @Author  : 之落花--falling_flowers
# @File    : demo.py
# @Software: PyCharm
from wcferry import Wcf

from GPT import GPT
from Command import gpt
from suswx import Robot, Content, Configuration


def main():
    config: Configuration = Configuration("./config.yaml")
    wcf: Wcf = Wcf(debug=True)
    sus: Robot = Robot(wcf)
    sus.register(GPT(wcf, config).private_reply, Content.TEXT, fromFriend=True)
    sus.register_command(gpt(wcf, config))
    sus.run()


if __name__ == "__main__":
    main()
