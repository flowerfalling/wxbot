# -*- coding: utf-8 -*-
# @Time    : 2023/12/15 11:14
# @Author  : 之落花--falling_flowers
# @File    : Command.py
# @Software: PyCharm
import logging
import re
import typing

import wcferry

from suswx import Configuration


class Administrator(object):
    """
    Operate robot functions and control other people’s permissions
    """

    HELP_DOCS: str = """Administrator documentation
  /help 获取帮助
  /state 查看功能状态
  /disable|enable name1[,name2[...]] func1[,func2[...]] 开启|禁止某人某功能权限
  /start|stop func1[,func2[,func3[...]] 开启|停止功能"""

    def __init__(self, wcf: wcferry.Wcf, config: Configuration, logger: logging.Logger, admin: str = None) -> None:
        """
        :param wcf: your wcf instance
        :param config: your configuration
        :param logger: the logger instance
        """
        self.__wcf: wcferry.Wcf = wcf
        self.__config: Configuration = config
        self.__logger: logging.Logger = logger
        self.__admin: str = admin if admin else self.__wcf.get_self_wxid()

    def __call__(self, msg: wcferry.WxMsg) -> None:
        """
        Function to process command
        :param msg: the command message
        """
        if msg.content == "/help":
            self.__wcf.send_text(self.HELP_DOCS, self.__admin)
        elif msg.content == "/state":
            funcs: typing.Iterable = self.__config.config.keys()
            self.__wcf.send_text(
                "  STATE\n" + "".join(
                    (f"- {i}: {'enable' if self.__config[i]['enable'] else 'disable'}\n" for i in funcs)),
                self.__admin)
        elif c := re.fullmatch("/(enable|disable) (.*?) (.*?)", msg.content):
            command: tuple = c.groups()
            mode: str = command[0]
            users: list[str] = command[1].split(",")
            funcs: list[str] = command[2].split(",")
            self.update_access(users, funcs, mode)
        elif c := re.fullmatch("/(start|stop) (.*?)", msg.content):
            command: tuple = c.groups()
            mode: str = command[0]
            funcs: list[str] = command[1].split(",")
            for f in funcs:
                if self.__config[f] is None:
                    self.__wcf.send_text(info := f"function {f} does not exist", self.__admin)
                    self.__logger.info(info)
                    continue
                self.__config[f]["enable"] = mode == 'start'
                self.__wcf.send_text(info := f"{f} has been turned {'on' if mode == 'start' else 'off'}", self.__admin)
                self.__logger.info(info)
        self.__config.save_config()

    def update_access(self, users: list[str], funcs: typing.Iterable[str], mode: str) -> None:
        """
        Change user permissions for specific features
        :param users: List of usernames
        :param funcs: Function name list
        :param mode: enable/disable
        """
        contacts: list[dict] = self.__wcf.get_friends()
        contacts.append(self.__wcf.get_info_by_wxid(self.__wcf.get_self_wxid()))
        if stranger := set(users) - {i['name'] for i in contacts}:
            self.__wcf.send_text(info := f"{stranger} are not your friends, please check the username", self.__admin)
            self.__logger.info(info)
        if funcs == ['all']:
            funcs = self.__config.config.keys()
        for f in funcs:
            if self.__config[f] is None:
                self.__wcf.send_text(info := f"function {f} does not exist", self.__admin)
                self.__logger.info(info)
                continue
            for i in contacts:
                if i["name"] in users:
                    if mode == "enable":
                        if i["wxid"] not in self.__config[f]["access"]:
                            self.__config[f]["access"].append(i["wxid"])
                            self.__wcf.send_text(info := f"The {f} access has been turned on for user [{i['name']}]", self.__admin)
                        else:
                            self.__wcf.send_text(info := f"The user [{i['name']}]'s {f} access already exists", self.__admin)
                    elif mode == "disable":
                        if i["wxid"] in self.__config[f]["access"]:
                            self.__config[f]["access"].remove(i["wxid"])
                            self.__wcf.send_text(info := f"The {f} access has been turned off for user [{i['name']}]", self.__admin)
                        else:
                            self.__wcf.send_text(info := f"The user [{i['name']}]'s {f} access no longer exists", self.__admin)
                    else:
                        continue
                    self.__logger.info(info)
