# -*- coding: utf-8 -*-
# @Time    : 2023/12/16 10:19
# @Author  : 之落花--falling_flowers
# @File    : plugins.py
# @Software: PyCharm
import asyncio

import aiohttp
from wcferry import WxMsg

from plugins import register
from suswx.common import wcf, logger


@register(fromFriend=True, mode="async", check=[lambda msg: msg.content == "@一言"])
async def hitokoto(msg: WxMsg) -> None:
    """
    Hitokoto, represents the touch of words and the communication of souls
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://v1.hitokoto.cn") as resp:
                r = await asyncio.wait_for(resp.json(), timeout=5)
                wcf.send_text(info := f'{r["hitokoto"]}\n----{r["from"]}[{r["from_who"]}]', msg.sender)
    except asyncio.TimeoutError:
        wcf.send_text(info := "Sorry, hitokoto timed out", msg.sender)
    logger.info(info)

