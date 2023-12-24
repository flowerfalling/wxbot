# -*- coding: utf-8 -*-
# @Time    : 2023/12/16 10:19
# @Author  : 之落花--falling_flowers
# @File    : funcs.py
# @Software: PyCharm
import logging
from typing import Callable

import requests
import wcferry

from suswx import Configuration

__all__ = ["hitokoto", "menu"]


def hitokoto(
        wcf: wcferry.Wcf, config: Configuration, logger: logging.Logger
) -> Callable[[wcferry.WxMsg], None]:
    """
    hitokoto func that can be used to send a sentence for WeChat
    :param wcf: your wcf instance
    :param config: your configuration
    :param logger: a logger to record command information
    :return: A callable hitokoto to register in the robot
    """

    def process(msg: wcferry.WxMsg) -> None:
        """
        the process method for hitokoto sending sentence
        :param msg: Pending self's message
        """
        if all(
                (
                        msg.sender in config["hitokoto"]["access"],
                        config["hitokoto"]["enable"],
                        msg.content == "@一言",
                )
        ):
            resp: dict = requests.get("https://v1.hitokoto.cn", timeout=3).json()
            wcf.send_text(
                response := f'{resp["hitokoto"]}\n----{resp["from"]}[{resp["from_who"]}]',
                msg.sender,
            )
            logger.info(response.replace('\n', '\\n'))

    return process


def menu(
        wcf: wcferry.Wcf, config: Configuration, logger: logging.Logger
) -> Callable[[wcferry.WxMsg], None]:
    """
    menu func that can be used to send func list for WeChat
    :param wcf: your wcf instance
    :param config: your configuration
    :param logger: a logger to record command information
    :return: A callable hitokoto to register in the robot
    """
    MENU = '''- /gpt help
- %gemini help
- @一言
- @菜单'''

    def process(msg: wcferry.WxMsg) -> None:
        """
        the process method for menu sending sentence
        :param msg: Pending self's message
        """
        if all(
                (
                        msg.sender in config["menu"]["access"],
                        config["menu"]["enable"],
                        msg.content == "@菜单",
                )
        ):
            wcf.send_text(MENU, msg.sender)
            logger.info("send menu message")

    return process
