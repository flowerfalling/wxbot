# -*- coding: utf-8 -*-
# @Time    : 2023/12/15 11:14
# @Author  : 之落花--falling_flowers
# @File    : Command.py
# @Software: PyCharm
import logging
import re
from typing import Callable

import wcferry

from suswx import Configuration


def gpt(wcf: wcferry.Wcf, config: Configuration, logger: logging.Logger) -> Callable[[wcferry.WxMsg], None]:
    """
    A method for only administrator to operate gpt processing commands
    :param wcf: your wcf instance
    :param config: your configuration of gpt
    :return: A callable to register in the robot
    """
    gpt_help: str = """gpt command[me]
  /gpt start 开启gpt
  /gpt stop 关闭gpt
  /gpt enable username 开启用户gpt权限
  /gpt disable username 关闭用户gpt权限
  /gpt help 获取帮助"""

    def process(msg: wcferry.WxMsg) -> None:
        """
        the process method for gpt processing commands
        :param msg: Pending self's message
        """
        if not msg.content.startswith("/gpt"):
            return
        me: str = wcf.get_self_wxid()
        cmm: str = msg.content
        if cmm == "/gpt":
            wcf.send_text('send "/gpt help" to get help docs', me)
        elif r := re.fullmatch(r"/gpt ([^ ]*?)", msg.content):
            r = r.groups()
            match r[0]:
                case "help":
                    wcf.send_text(gpt_help, me)
                case "stop":
                    config.chatgpt["enable"] = False
                    config.save_config()
                    logger.info("GPT has been stopped")
                case "start":
                    config.chatgpt["enable"] = True
                    config.save_config()
                    logger.info("GPT has been turned on")
        elif r := re.fullmatch("/gpt (.*?) (.*?)", cmm):
            r = r.groups()
            match r[0]:
                case "enable":
                    for i in wcf.get_friends():
                        if i["name"] == r[1] and r[1] not in config.chatgpt:
                            config.chatgpt["allow_list"].append(i["wxid"])
                            config.save_config()
                            logger.info("已为用户[%s]开启gpt权限", r[1])
                case "disable":
                    for i in wcf.get_friends():
                        if i["name"] == r[1] and r[1] in config.chatgpt:
                            config.chatgpt.remove(i["wxid"])
                            config.save_config()
                            logger.info("已为用户[%s]关闭gpt权限", r[1])

    return process
