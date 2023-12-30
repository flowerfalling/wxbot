# -*- coding: utf-8 -*-
# @Time    : 2023/12/29 20:38
# @Author  : 之落花--falling_flowers
# @File    : common.py
# @Software: PyCharm
import logging

from wcferry import Wcf

__all__ = ["wcf", "logger", "admin_wxid"]

wcf: Wcf = Wcf()
logger: logging.Logger = logging.getLogger()
admin_wxid: list[str] = [wcf.get_self_wxid()]
