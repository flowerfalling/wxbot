# -*- coding: utf-8 -*-
# @Time    : 2023/12/26 21:44
# @Author  : 之落花--falling_flowers
# @File    : menu.py
# @Software: PyCharm
import wcferry

from Configuration import config
from plugins import init
from suswx.bot import register
from suswx.common import wcf, logger

MENU = '''- /gpt help
- %gemini help
- @一言
- @菜单'''


@init()
@register(fromFriend=True)
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
