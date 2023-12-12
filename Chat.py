# -*- coding: utf-8 -*-
# @Time    : 2023/12/10 12:31
# @Author  : 之落花--falling_flowers
# @File    : Chat.py
# @Software: PyCharm
import wcferry

from GPT import GPT


class Chat(object):
    wxid: str = None
    name: str = None
    code: str = None
    city: str = None
    province: str = None
    country: str = None
    gender: str = None
    remark: str = None

    gpt: GPT = GPT()

    def __init__(self, info: dict, wcf: wcferry.Wcf) -> None:
        self.wcf = wcf
        self.__dict__.update(info)

    def gpt_reply(self, msg: wcferry.WxMsg) -> str:
        if msg.from_group():
            self.wcf.send_text(
                resp := f"GPT:{self.gpt(msg.content[1:])}@", msg.roomid, msg.sender
            )
        else:
            self.wcf.send_text(resp := f"GPT:{self.gpt(msg.content[1:])}", msg.sender)
        return resp


def main():
    pass


if __name__ == "__main__":
    main()
