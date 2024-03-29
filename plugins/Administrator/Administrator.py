# -*- coding: utf-8 -*-
# @Time    : 2023/12/15 11:14
# @Author  : 之落花--falling_flowers
# @File    : Administrator.py
# @Software: PyCharm
import re
from typing import Sequence, Literal

from wcferry import WxMsg

import plugins
from Configuration import config
from plugins import register, plugins_registry, save_func_config
from suswx.bot import registry
from suswx.common import wcf, logger, botadmin

__all__ = ["admin"]

update_access_mode = Literal["enable", "disable"]
switch_func_mode = Literal["start", "stop"]


class Administrator(object):
    """
    Operate robot functions and control other people’s permissions
    """

    HELP_DOCS: str = """Administrator documentation
  /help 获取帮助
  /state 查看功能状态
  /disable|enable name1[,name2[...]] func1[,func2[...]] 开启|禁止某人某功能权限
  /start|stop func1[,func2[,func3[...]] 开启|停止功能
  /admin name 转移管理员身份
  /config 重新加载配置文件
  /quit 退出机器人"""

    def __call__(self, msg: WxMsg) -> None:
        """
        Function to process command
        :param msg: the command message
        """
        if msg.content == "/help":
            wcf.send_text(self.HELP_DOCS, botadmin.wxid)
        elif msg.content == "/state":
            wcf.send_text("  STATE" + "".join(
                (f"\n- {i.name}: {'enable' if i.enable else 'disable'}"
                 for i in registry if i not in plugins_registry["frozen"])
            ), botadmin.wxid)
        elif msg.content == "/config":
            config.load_config()
            plugins.load()
            for f in plugins_registry["save"]:
                func_info: dict = config["plugins"]["info"][f.name]
                f.access = set(func_info["access"])
                f.enable = func_info["enable"]
            wcf.send_text(info := "Configuration reloaded", botadmin.wxid)
            logger.info(info)
        elif c := re.fullmatch("/admin (.*?)", msg.content):
            admin_name: str = c.groups()[0]
            contacts: list[dict] = wcf.get_friends()
            contacts.append(wcf.get_info_by_wxid(wcf.get_self_wxid()))
            new_admin = list(filter(lambda i: i["name"] == admin_name, contacts))
            if len(new_admin) == 1:
                config["administrator"]["name"] = new_admin[0]["name"]
                botadmin.wxid = config["administrator"]["wxid"] = new_admin[0]["wxid"]
                registry["ADMIN"].access = {botadmin.wxid}
                wcf.send_text(info := f"Administrator rights have been transferred to user {admin_name}", msg.sender)
            elif len(new_admin) == 0:
                wcf.send_text(info := f"You do not have a user named {admin_name}, please check the username", botadmin.wxid)
            else:
                wcf.send_text(info := f"You have more than one friend named {admin_name}. Please make sure the username of the user you want to transfer administrator rights to is unique.", botadmin.wxid)
            logger.info(info)
        elif c := re.fullmatch("/(enable|disable) (.*?) (.*?)", msg.content):
            command: tuple = c.groups()
            mode: update_access_mode = command[0]
            users: set[str] = set(command[1].split(","))
            funcs: set[str] = set(command[2].split(","))
            self.update_access(users, funcs, mode)
        elif c := re.fullmatch("/(start|stop) (.*?)", msg.content):
            command: tuple = c.groups()
            mode: switch_func_mode = command[0]
            funcs: list[str] = command[1].split(",")
            self.switch_func(funcs, mode)
        save_func_config()

    @staticmethod
    def update_access(users: set[str], funcs: set[str], mode: update_access_mode) -> None:
        """
        Change user permissions for specific features
        :param users: List of usernames
        :param funcs: Function name list
        :param mode: enable/disable
        """
        contacts: list[dict] = wcf.get_friends()
        contacts.append(wcf.get_info_by_wxid(wcf.get_self_wxid()))
        if stranger := users - {i['name'] for i in contacts}:
            wcf.send_text(info := f"{stranger} are not your friends, please check the username", botadmin.wxid)
            logger.info(info)
        users -= stranger
        users_wxid = {i["wxid"] for i in contacts if i["name"] in users}
        if funcs == {"all"}:
            funcs = [i.name for i in registry if i not in plugins_registry["frozen"]]
        func_names = []
        for f in funcs:
            if not (func := registry[f]):
                wcf.send_text(info := f"function {f} does not exist", botadmin.wxid)
                logger.info(info)
                continue
            if func in plugins_registry["frozen"]:
                continue
            if mode == "enable":
                func.access.update(users_wxid)
            elif mode == "disable":
                func.access.difference_update(users_wxid)
            func_names.append(f)
        if func_names:
            wcf.send_text(
                info := f"The {func_names} access has been turned {'on' if mode == 'enable' else 'off'} for user {users}",
                botadmin.wxid
            )
            logger.info(info)

    @staticmethod
    def switch_func(funcs: Sequence[str], mode: switch_func_mode) -> None:
        """
        Set robot function switch
        :param funcs: function name sequence
        :param mode: enable/disable
        """
        for f in funcs:
            if not (func := registry[f]):
                wcf.send_text(info := f"function {f} does not exist", botadmin.wxid)
            elif func in plugins_registry["frozen"]:
                wcf.send_text(info := f"frozen function {f} cannot be turned on or off", botadmin.wxid)
            else:
                func.enable = mode == "start"
                wcf.send_text(info := f"{f} has been turned {'on' if mode == 'start' else 'off'}", botadmin.wxid)
            logger.info(info)


admin: Administrator = Administrator()


@register(fromAdmin=True, name="ADMIN", access={botadmin.wxid}, frozen=True)
def admin_func(msg: WxMsg) -> None:
    admin(msg)
