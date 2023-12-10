# -*- coding: utf-8 -*-
# @Time    : 2023/12/10 12:42
# @Author  : 之落花--falling_flowers
# @File    : Middleware.py
# @Software: PyCharm
from Chat import Chat, Info


class Middleware(object):
    def __init__(self, contacts: list[dict]):
        self.contacts = [Chat(Info(i)) for i in contacts]

    def search_with_wxid(self, wxid: str) -> Chat | None:
        for i in self.contacts:
            if i.info.wxid == wxid:
                return i

    def search_with_name(self, name: str) -> list[Chat]:
        chats = []
        for i in self.contacts:
            if i.info.name == name:
                chats.append(i)
        return chats


def main():
    pass


if __name__ == '__main__':
    main()
