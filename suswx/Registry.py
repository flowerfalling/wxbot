# -*- coding: utf-8 -*-
# @Time    : 2023/12/28 23:19
# @Author  : 之落花--falling_flowers
# @File    : Registry.py
# @Software: PyCharm
from typing import Callable, Literal, Sequence, Optional

from wcferry import WxMsg

from suswx import Content

func_startup_mode = Literal["mt", "async"]

__all__ = ["Registry", "ProcessMsgFunc", "func_startup_mode"]


class ProcessMsgFunc(object):
    def __init__(
            self,
            func: Callable[[WxMsg], None],
            name: str,
            msgType: Sequence[Content],
            fromfriend: bool,
            fromgroup: bool,
            fromadmin: bool,
            mode: func_startup_mode,
            enable: bool,
            access: set,
    ) -> None:
        """
        Message processing functions within the registry
        :param func: a callable to process message
        :param name: Function name
        :param msgType: Message types allowed to be processed
        :param fromfriend: Whether to handle messages from friends
        :param fromgroup: Whether to handle messages from groups
        :param fromadmin: Whether to handle messages from the admin
        :param mode: Function startup method (multithreaded "mt" or asynchronous "async")
        :param enable: Whether to enable
        :param access: The set of wxids of allowed message senders
        """
        self.func: Callable[[WxMsg], None] = func
        self.name: str = name
        self.msgtype: set = set([i.value for i in msgType])
        self.fromfriend: bool = fromfriend
        self.fromgroup: bool = fromgroup
        self.fromadmin: bool = fromadmin
        self.match: list = [self.fromfriend, self.fromgroup, self.fromadmin]
        self.mode: func_startup_mode = mode
        self.enable: bool = enable
        self.access = access

    def check(self, msg: WxMsg, admin: str) -> bool:
        """
        Check whether the message initially meets the requirements
        :param msg: Messages to be checked
        :param admin: Administrator's wxid
        :return: whether the message meets the requirements
        """
        from_group: bool = msg.from_group()
        from_admin: bool = msg.sender == admin
        from_friend: bool = not (from_admin or from_group)
        source: list = [from_friend, from_group, from_admin]
        if all((
                self.enable,
                msg.type in self.msgtype,
                [i and j for (i, j) in zip(source, self.match)] == self.match,
                msg.sender in self.access or "ALL" in self.access
        )):
            return True
        return False

    def __hash__(self) -> int:
        return hash(self.name)


class Registry(object):
    def __init__(self):
        self._registry: set[ProcessMsgFunc] = set()
        self.mt: set[ProcessMsgFunc] = set()
        self.acync: set[ProcessMsgFunc] = set()

    def add(self, func: ProcessMsgFunc) -> None:
        """
        Add entries to the registry
        :param func: the ProcessMsgFunc instance
        """
        self._registry.add(func)
        if func.mode == 'mt':
            self.mt.add(func)
        elif func.mode == 'async':
            self.acync.add(func)
        else:
            raise ValueError(f"Wrong startup method {func.mode}")

    @property
    def names(self) -> list[str]:
        """
        :return: The names of all functions in the registry
        """
        return [i.name for i in self._registry]

    def __getitem__(self, name) -> Optional[ProcessMsgFunc]:
        if item := list(filter(lambda i: i.name == name, self._registry)):
            return item[0]
        else:
            return None

    def __iter__(self):
        return iter(self._registry)
