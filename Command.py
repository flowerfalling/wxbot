# -*- coding: utf-8 -*-
# @Time    : 2023/12/15 11:14
# @Author  : 之落花--falling_flowers
# @File    : Command.py
# @Software: PyCharm
import re

import wcferry

from suswx import Configuration


def gpt(wcf: wcferry.Wcf, config: Configuration):
    gpt_help = """gpt command[me]
  /gpt start 开启gpt
  /gpt stop 关闭gpt
  /gpt enable username 开启用户gpt权限
  /gpt disable username 关闭用户gpt权限
  /gpt help 获取帮助"""

    def process(msg: wcferry.WxMsg):
        if not msg.content.startswith("/gpt"):
            return
        me = wcf.get_self_wxid()
        cmm = msg.content
        if cmm == "/gpt":
            wcf.send_text('发送"/gpt help"获取帮助', me)
        elif r := re.fullmatch(r"/gpt ([^ ]*?)", msg.content):
            r = r.groups()
            match r[0]:
                case "help":
                    wcf.send_text(gpt_help, me)
                case "stop":
                    config.chatgpt["enable"] = False
                    config.save_config()
                case "start":
                    config.chatgpt["enable"] = True
                    config.save_config()
        elif (r := re.fullmatch("/gpt (.*?) (.*?)", cmm)) is not None:
            r = r.groups()
            match r[0]:
                case "enable":
                    for i in wcf.get_friends():
                        if i["name"] == r[1] and r[1] not in config.chatgpt:
                            config.chatgpt["allow_list"].append(i["wxid"])
                            config.save_config()
                            print(f"已为用户[{r[1]}]开启gpt权限")
                case "disable":
                    for i in wcf.get_friends():
                        if i["name"] == r[1] and r[1] in config.chatgpt:
                            config.chatgpt.remove(i["wxid"])
                            config.save_config()
                            print(f"已为用户[{r[1]}]开启gpt权限")

    return process
