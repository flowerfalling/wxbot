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


def gpt(
        wcf: wcferry.Wcf, config: Configuration, logger: logging.Logger
) -> Callable[[wcferry.WxMsg], None]:
    """
    A method for only administrator to operate gpt processing commands
    :param wcf: your wcf instance
    :param config: your configuration
    :param logger: a logger to record command information
    :return: A callable gpt-control to register in the robot
    """

    def process(msg: wcferry.WxMsg) -> None:
        """
        the process method for gpt processing commands
        :param msg: Pending self's message
        """
        _control(wcf, msg, "/gpt", config, logger)

    return process


def gemini(
        wcf: wcferry.Wcf, config: Configuration, logger: logging.Logger
) -> Callable[[wcferry.WxMsg], None]:
    """
    A method for only administrator to operate Gemini processing commands
    :param wcf: your wcf instance
    :param config: your configuration
    :param logger: a logger to record command information
    :return: A callable Gemini-control to register in the robot
    """

    def process(msg: wcferry.WxMsg) -> None:
        """
        the process method for Gemini processing commands
        :param msg: Pending self's message
        """
        _control(wcf, msg, "/gemini", config, logger)

    return process


def hitokoto(
        wcf: wcferry.Wcf, config: Configuration, logger: logging.Logger
) -> Callable[[wcferry.WxMsg], None]:
    """
    A method for only administrator to operate hitokoto processing commands
    :param wcf: your wcf instance
    :param config: your configuration
    :param logger: a logger to record command information
    :return: A callable hitokoto-control to register in the robot
    """

    def process(msg: wcferry.WxMsg) -> None:
        """
        the process method for hitokoto processing commands
        :param msg:
        """
        _control(wcf, msg, "/hitokoto", config, logger)

    return process


def menu(
        wcf: wcferry.Wcf, config: Configuration, logger: logging.Logger
) -> Callable[[wcferry.WxMsg], None]:
    """
    A method for only administrator to operate hitokoto processing commands
    :param wcf: your wcf instance
    :param config: your configuration
    :param logger: a logger to record command information
    :return: A callable hitokoto-control to register in the robot
    """

    def process(msg: wcferry.WxMsg) -> None:
        """
        the process method for hitokoto processing commands
        :param msg:
        """
        _control(wcf, msg, "/menu", config, logger)

    return process


def _control(
        wcf: wcferry.Wcf,
        msg: wcferry.WxMsg,
        key: str,
        config: Configuration,
        logger: logging.Logger,
) -> None:
    """
    The _control function is an internal part of the software that governs how the program responds to certain message content.

    It uses a specified key to control different functionality including the start and stop commands, as well as enabling or disabling certain users.
    :param wcf: your wcf instance
    :param msg: Pending self's message
    :param key: Keywords of the command, such as /gpt (corresponding in config.yaml)
    :param config: your configuration
    :param logger: a logger to record command information
    """
    if not msg.content.startswith(key):
        return
    me: str = wcf.get_self_wxid()
    k: str = key[1:]
    if (cmm := msg.content) == key:
        wcf.send_text(f'send "{key} help" to get help docs', me)
    elif cmm == f"{key} start":
        config.__getattr__(k)["enable"] = True
        config.save_config()
        logger.info(f"{k} has been turned on")
    elif cmm == f"{key} stop":
        config.__getattr__(k)["enable"] = False
        config.save_config()
        logger.info(f"{k} has been stopped")
    elif cmm == f"{key} help":
        help_docs = f"""{k} command[me]
  {key} start 开启gpt
  {key} stop 关闭gpt
  {key} enable username 开启用户{k}权限
  {key} disable username 关闭用户{k}权限
  {key} help 获取帮助"""
        wcf.send_text(help_docs, me)
    elif r := re.fullmatch(f"{key} (enable|disable) (.*?)", cmm):
        r = r.groups()
        allow_list = config.__getattr__(k)["allow_list"]
        for i in wcf.get_friends():
            if i["name"] == r[1] and (i['wxid'] in allow_list) ^ (m := r[0] == "enable"):
                allow_list.append(i['wxid']) if m else allow_list.remove(i['wxid'])
                config.save_config()
                logger.info(
                    "%s permission has been turned %s for user [%s]",
                    key, "on" if m else "off", r[1],
                )
