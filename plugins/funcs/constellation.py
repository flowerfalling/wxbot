# -*- coding: utf-8 -*-
# @Time    : 2024/1/14 15:45
# @Author  : 之落花--falling_flowers
# @File    : constellation.py
# @Software: PyCharm
import asyncio
import os
import re

import aiofiles
import aiohttp
from wcferry import WxMsg

from plugins import register
from suswx.common import wcf, logger


@register(fromFriend=True, mode="async", check=[lambda msg: msg.content.startswith("@星座运势")])
async def constellation(msg: WxMsg) -> None:
    """
    Return 10 hot searches on Zhihu or Weibo
    """
    constellation_set = ['水瓶', '双鱼', '白羊', '金牛', '双子', '巨蟹', '狮子', '处女', '天秤', '天蝎', '射手', '魔蝎']
    if c := re.match(f"@星座运势 ({'|'.join(constellation_set)})座*", msg.content):
        c = c.group(1)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://xiaoapi.cn/API/xzys_pic.php", params={'msg': c}) as resp:
                    async with aiofiles.open(f"{os.getcwd()}\\resource\\image\\{c}.jpeg", "wb") as f:
                        await f.write(await resp.read())
                    wcf.send_image(f"{os.getcwd()}\\resource\\image\\{c}.jpeg", msg.sender)
        except asyncio.TimeoutError:
            wcf.send_text(info := "Sorry, hot search timed out", msg.sender)
            logger.info(info)
