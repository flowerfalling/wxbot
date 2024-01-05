# -*- coding: utf-8 -*-
# @Time    : 2023/12/16 10:19
# @Author  : 之落花--falling_flowers
# @File    : plugins.py
# @Software: PyCharm
import wcferry

from Configuration import config
from plugins import init
from suswx.bot import register
from suswx.common import wcf, logger
import aiohttp


@init()
@register(fromFriend=True, mode="async")
async def hitokoto(msg: wcferry.WxMsg) -> None:
    """
    Hitokoto, represents the touch of words and the communication of souls
    """
    if all(
            (
                    msg.sender in config["plugins"]["info"]["hitokoto"]["access"],
                    config["plugins"]["info"]["hitokoto"]["enable"],
                    msg.content == "@一言",
            )
    ):
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
            async with session.get("https://v1.hitokoto.cn") as resp:
                r = await resp.json()
                wcf.send_text(info := f'{r["hitokoto"]}\n----{r["from"]}[{r["from_who"]}]', msg.sender)
                logger.info(info)
