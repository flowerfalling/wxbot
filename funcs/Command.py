# -*- coding: utf-8 -*-
# @Time    : 2023/12/15 11:14
# @Author  : 之落花--falling_flowers
# @File    : Command.py
# @Software: PyCharm
import logging
import re

import wcferry

from suswx import Configuration


class Permission(object):
    HELP_DOCS = """Permission documentation
  /help 获取帮助
  /state 查看功能状态
  /disable|enable name1[,name2[,name3[...]]] func1[,func2[,func3[...]] 开启|禁止某人某功能权限
  /start|stop func1[,func2[,func3[...]] 开启|停止功能
    """

    def __init__(self, wcf: wcferry.Wcf, config: Configuration, logger: logging.Logger) -> None:
        self.__wcf = wcf
        self.__config = config
        self.__logger = logger

    def __call__(self, msg: wcferry.WxMsg) -> None:
        if msg.content == "/help":
            self.__wcf.send_text(self.HELP_DOCS, self.__wcf.get_self_wxid())
        elif msg.content == "/state":
            funcs = self.__config.config.keys()
            self.__wcf.send_text(
                "  STATE\n" + "".join((f"- {i}: {'enable' if self.__config[i]['enable'] else 'disable'}\n" for i in funcs)),
                self.__wcf.get_self_wxid())
        elif c := re.fullmatch("/(enable|disable) (.*?) (.*?)", msg.content):
            command = c.groups()
            mode = command[0]
            users = command[1].split(",")
            funcs = command[2].split(",")
            self.update_access(users, funcs, mode)
        elif c := re.fullmatch("/(start|stop) (.*?)", msg.content):
            command = c.groups()
            mode = command[0]
            funcs = command[1].split(",")
            for f in funcs:
                if self.__config[f] is None:
                    self.__logger.info(f"function {f} does not exist")
                    continue
                self.__config[f]["enable"] = mode == 'start'
                self.__logger.info(f"{f} has been turned {'on' if mode == 'start' else 'off'}")
        self.__config.save_config()

    def update_access(self, users: list[str], funcs: list[str], mode: str) -> None:
        my_friends = self.__wcf.get_friends()
        if stranger := set(users) - {i['name'] for i in my_friends}:
            self.__logger.info(f"{stranger} are not your friends, please check the username")
        for f in funcs:
            if self.__config[f] is None:
                self.__logger.info(f"function {f} does not exist")
                continue
            for i in my_friends:
                if i["name"] in users:
                    if mode == "enable":
                        if i["wxid"] not in self.__config[f]["access"]:
                            self.__config[f]["access"].append(i["wxid"])
                            self.__logger.info(f"The {f} access has been turned on for user [{i['name']}]")
                        else:
                            self.__logger.info(f"The user [{i['name']}]'s {f} access already exists")
                    elif mode == "disable":
                        if i["wxid"] in self.__config[f]["access"]:
                            self.__config[f]["access"].remove(i["wxid"])
                            self.__logger.info(f"The {f} access has been turned off for user [{i['name']}]")
                        else:
                            self.__logger.info(f"The user [{i['name']}]'s {f} access no longer exists")
