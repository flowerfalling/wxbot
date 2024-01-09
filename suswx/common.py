# -*- coding: utf-8 -*-
# @Time    : 2023/12/29 20:38
# @Author  : 之落花--falling_flowers
# @File    : common.py
# @Software: PyCharm
import atexit
import logging

from wcferry import Wcf

__all__ = ["wcf", "logger", "admin_wxid", "botadmin", "Admin"]

wcf: Wcf = Wcf()
logger: logging.Logger = logging.getLogger()
admin_wxid: list[str] = [wcf.get_self_wxid()]
atexit.register(wcf.cleanup)
atexit.register(lambda: print("Quit done"))

logging.basicConfig(
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO,
)


class Admin(object):
    def __init__(self):
        self.wxid = wcf.get_self_wxid()


botadmin: Admin = Admin()
