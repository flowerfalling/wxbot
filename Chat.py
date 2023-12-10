# -*- coding: utf-8 -*-
# @Time    : 2023/12/10 12:31
# @Author  : 之落花--falling_flowers
# @File    : Chat.py
# @Software: PyCharm
from gpt import GPT


class Info(object):
    def __init__(self, info: dict):
        self.wxid = None
        self.name = None
        self.code = None
        self.city = None
        self.province = None
        self.country = None
        self.gender = None
        self.remark = None
        self.__dict__.update(info)


class Chat(object):
    def __init__(self, info: Info):
        self.info = info
        self.gpt: GPT


def main():
    pass


if __name__ == '__main__':
    main()
