# -*- coding: utf-8 -*-
# @Time    : 2024/2/9 10:48
# @Author  : 之落花--falling_flowers
# @File    : bless.py
# @Software: PyCharm
import random

import wcferry

from plugins.NewYearWish.blessings import blessings
from plugins import register
from suswx.common import wcf, logger


def check(msg: wcferry.WxMsg) -> bool:
    for c in ("新年", "快乐", "春节", "安康", "出息", "龙年", "吉祥", "开心", "祝", "福", "新的一年", 'happy', 'year'):
        if c in msg.content.lower():
            return True
    return False


@register(fromFriend=True, access={"ALL"}, check=[check])
def bless(msg: wcferry.WxMsg) -> None:
    wcf.send_text(info := random.choice(blessings), msg.sender)
    logger.info(info)
