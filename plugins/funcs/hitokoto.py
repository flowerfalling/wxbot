# -*- coding: utf-8 -*-
# @Time    : 2023/12/16 10:19
# @Author  : 之落花--falling_flowers
# @File    : plugins.py
# @Software: PyCharm
import requests
import wcferry

from Configuration import config
from plugins import init
from suswx.bot import register
from suswx.common import wcf, logger


@init()
@register(fromFriend=True)
def hitokoto(msg: wcferry.WxMsg) -> None:
    if all(
            (
                    msg.sender in config["plugins"]["info"]["hitokoto"]["access"],
                    config["plugins"]["info"]["hitokoto"]["enable"],
                    msg.content == "@一言",
            )
    ):
        resp: dict = requests.get("https://v1.hitokoto.cn", timeout=3).json()
        wcf.send_text(
            response := f'{resp["hitokoto"]}\n----{resp["from"]}[{resp["from_who"]}]',
            msg.sender,
        )
        logger.info(response)
