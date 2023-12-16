# -*- coding: utf-8 -*-
# @Time    : 2023/12/16 10:19
# @Author  : 之落花--falling_flowers
# @File    : funcs.py
# @Software: PyCharm
import logging
from typing import Callable

import requests
import wcferry

from suswx import Configuration


def hitokoto(
        wcf: wcferry.Wcf, config: Configuration, logger: logging.Logger
) -> Callable[[wcferry.WxMsg], None]:
    """
    hitokoto func that can be used to send a sentence for WeChat
    :param wcf: your wcf instance
    :param config: your configuration
    :param logger: a logger to record command information
    :return: A callable hitokoto to register in the robot
    """

    def process(msg: wcferry.WxMsg) -> None:
        """
        the process method for hitokoto sending sentence
        :param msg: Pending self's message
        """
        if all(
                (
                        msg.sender in config.hitokoto["allow_list"],
                        config.hitokoto["enable"],
                        msg.content == "@一言",
                )
        ):
            resp = requests.get("v1.hitokoto.cn", timeout=3).json()
            wcf.send_text(
                response := f'{resp["hitokoto"]}\n--{resp["from"]}[{resp["from_who"]}]',
                msg.sender,
            )
            logger.info(response)

    return process
