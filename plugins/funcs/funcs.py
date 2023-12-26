# -*- coding: utf-8 -*-
# @Time    : 2023/12/16 10:19
# @Author  : 之落花--falling_flowers
# @File    : plugins.py
# @Software: PyCharm
import requests
import wcferry

import suswx
from Configuration import config

__all__ = ["hitokoto", "menu"]


MENU = '''- /gpt help
- %gemini help
- @一言
- @菜单'''


def menu(msg: wcferry.WxMsg) -> None:
    if all(
            (
                    msg.sender in config["plugins"]["menu"]["access"],
                    config["plugins"]["menu"]["enable"],
                    msg.content == "@菜单",
            )
    ):
        suswx.wcf.send_text(MENU, msg.sender)
        suswx.logger.info("send menu message")


def hitokoto(msg: wcferry.WxMsg) -> None:
    if all(
            (
                    msg.sender in config["plugins"]["hitokoto"]["access"],
                    config["plugins"]["hitokoto"]["enable"],
                    msg.content == "@一言",
            )
    ):
        resp: dict = requests.get("https://v1.hitokoto.cn", timeout=3).json()
        suswx.wcf.send_text(
            response := f'{resp["hitokoto"]}\n----{resp["from"]}[{resp["from_who"]}]',
            msg.sender,
        )
        suswx.logger.info(response)
