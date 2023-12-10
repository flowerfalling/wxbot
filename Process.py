# -*- coding: utf-8 -*-
# @Time    : 2023/12/10 15:02
# @Author  : 之落花--falling_flowers
# @File    : Process.py
# @Software: PyCharm
import wcferry

import Config
from Contacts import Contacts
from Chat import Chat


class Process(object):
    def __init__(self, wcf: wcferry.Wcf) -> None:
        self.contacts = Contacts(wcf)

    def process(self, msg: wcferry.WxMsg) -> None:
        content = msg.content
        chat = self.contacts.search_with_wxid(msg.sender)
        if msg.from_self():
            return
        elif msg.from_group():
            return
        if content.startswith('/'):
            if chat.name in Config.GPT['Users']:
                resp = chat.gpt_reply(msg)
                self.log(chat, resp, 'GPT')

    @staticmethod
    def log(chat: Chat, resp: str, signal: str = '') -> None:
        print(f'[{signal}]\t->\t[{chat.name}]\t|{resp}')


def main():
    pass


if __name__ == '__main__':
    main()
