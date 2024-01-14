# -*- coding: utf-8 -*-
# @Time    : 2023/12/26 21:44
# @Author  : 之落花--falling_flowers
# @File    : menu.py
# @Software: PyCharm
import wcferry

from plugins import register
from suswx.common import wcf, logger

MENU = '''- /gpt help
- %gemini help
- @一言
- @菜单
- @历史上的今天
- @微博/知乎热搜
- @星座运势 xxx'''


@register(fromFriend=True, check=[lambda msg: msg.content == "@菜单"])
def menu(msg: wcferry.WxMsg) -> None:
    """
    function list
    """
    wcf.send_text(MENU, msg.sender)
    logger.info("send menu message")
