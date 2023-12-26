# -*- coding: utf-8 -*-
# @Time    : 2023/12/26 21:44
# @Author  : 之落花--falling_flowers
# @File    : menu.py
# @Software: PyCharm
import wcferry

import suswx
from Configuration import config
from suswx import Content

MENU = '''- /gpt help
- %gemini help
- @一言
- @菜单'''


@suswx.register_func((Content.TEXT,), True)
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
