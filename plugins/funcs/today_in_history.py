# -*- coding: utf-8 -*-
# @Time    : 2024/1/14 15:18
# @Author  : 之落花--falling_flowers
# @File    : today_in_history.py
# @Software: PyCharm
import asyncio

import aiohttp
from wcferry import WxMsg

from plugins import register
from suswx.common import wcf, logger


@register(fromFriend=True, mode="async", check=[lambda msg: msg.content == "@历史上的今天"])
async def history(msg: WxMsg) -> None:
    """
    Return ten events from this day in history
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://xiaoapi.cn/API/lssdjt.php") as resp:
                wcf.send_text(info := await asyncio.wait_for(resp.text(), timeout=5), msg.sender)
    except asyncio.TimeoutError:
        wcf.send_text(info := "Sorry, today in history timed out", msg.sender)
    logger.info(info)
