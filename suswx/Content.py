# -*- coding: utf-8 -*-
# @Time    : 2023/12/15 10:12
# @Author  : 之落花--falling_flowers
# @File    : Content.py
# @Software: PyCharm
from enum import Enum

__all__ = ["Content"]


class Content(Enum):
    """
    Allowed WeChat message type for message processing (temporarily supported)
    """

    TEXT: int = 1
    PICTURE: int = 3
    AUDIO: int = 34
    VIDEO: int = 47
    FILE: int = 1090519089
