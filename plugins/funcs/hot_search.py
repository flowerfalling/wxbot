# -*- coding: utf-8 -*-
# @Time    : 2024/1/14 15:32
# @Author  : 之落花--falling_flowers
# @File    : hot_search.py
# @Software: PyCharm
import asyncio

import aiohttp
from wcferry import WxMsg

from plugins import register
from suswx.common import wcf, logger


@register(fromFriend=True, mode="async", check=[lambda msg: msg.content in ("@微博热搜", "@知乎热搜")])
async def hot_search(msg: WxMsg) -> None:
    """
    Return 10 hot searches on Zhihu or Weibo
    """
    search = "weibo" if msg.content[:2] == "微博" else "zhihu"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://xiaoapi.cn/API/resou.php", params={'type': search}) as resp:
                wcf.send_text(info := await asyncio.wait_for(resp.text(), timeout=5), msg.sender)
    except asyncio.TimeoutError:
        wcf.send_text(info := "Sorry, hot search timed out", msg.sender)
    logger.info(info)
