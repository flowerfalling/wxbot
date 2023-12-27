# -*- coding: utf-8 -*-
# @Time    : 2023/12/26 21:44
# @Author  : 之落花--falling_flowers
# @File    : menu.py
# @Software: PyCharm
import wcferry

from Configuration import config
from suswx import register_func, wcf, logger, Content

MENU = '''- /gpt help
- %gemini help
- @一言
- @菜单'''


@register_func((Content.TEXT,), True)
def menu(msg: wcferry.WxMsg) -> None:
    if all(
            (
                    msg.sender in config["plugins"]["info"]["menu"]["access"],
                    config["plugins"]["info"]["menu"]["enable"],
                    msg.content == "@菜单",
            )
    ):
        wcf.send_text(MENU, msg.sender)
        logger.info("send menu message")
