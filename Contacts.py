# -*- coding: utf-8 -*-
# @Time    : 2023/12/10 12:42
# @Author  : 之落花--falling_flowers
# @File    : Contacts.py
# @Software: PyCharm
from Chat import Chat
from wcferry import Wcf


class Contacts(object):
    def __init__(self, wcf: Wcf) -> None:
        self.contacts = [Chat(i, wcf) for i in wcf.get_friends()]
        self.contacts.append(Chat(wcf.get_info_by_wxid(wcf.get_self_wxid()), wcf))
        self.contacts[-1].remark = 'Me'

    def search_with_wxid(self, wxid: str) -> Chat:
        for i in self.contacts:
            if i.wxid == wxid:
                return i
        return self.contacts[-1]

    def search_with_name(self, name: str) -> list[Chat]:
        chats = []
        for i in self.contacts:
            if i.name == name:
                chats.append(i)
        return chats


def main():
    pass


if __name__ == '__main__':
    main()
