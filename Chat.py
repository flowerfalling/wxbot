# -*- coding: utf-8 -*-
# @Time    : 2023/12/10 12:31
# @Author  : 之落花--falling_flowers
# @File    : Chat.py
# @Software: PyCharm
import wcferry


class Chat(object):
    wxid: str = None
    name: str = None
    code: str = None
    city: str = None
    province: str = None
    country: str = None
    gender: str = None
    remark: str = None

    def __init__(self, info: dict, wcf: wcferry.Wcf) -> None:
        self.wcf = wcf
        self.__dict__.update(info)


def main():
    pass


if __name__ == "__main__":
    main()
