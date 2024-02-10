# -*- coding: utf-8 -*-
# @Time    : 2024/2/9 10:48
# @Author  : 之落花--falling_flowers
# @File    : bless.py
# @Software: PyCharm
import asyncio
import random

import wcferry

from plugins import register
from plugins.NewYearWish.blessings import blessings
from suswx.common import wcf, logger


def check(msg: wcferry.WxMsg) -> bool:
    for c in (
    "新年", "快乐", "春节", "安康", "除夕", "龙年", "过年", "吉祥", "开心", "祝", "福", "新的一年", 'happy', 'year'):
        if c in msg.content.lower():
            return True
    return False


@register(fromFriend=True, access={"ALL"}, mode="async", check=[check])
async def bless(msg: wcferry.WxMsg) -> None:
    await asyncio.sleep(1)
    wcf.send_text(info := random.choice(blessings), msg.sender)
    logger.info(info)
