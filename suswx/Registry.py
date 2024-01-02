# -*- coding: utf-8 -*-
# @Time    : 2023/12/28 23:19
# @Author  : 之落花--falling_flowers
# @File    : Registry.py
# @Software: PyCharm
import asyncio
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
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
            access: Optional[set],
    ) -> None:
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
        if access is None:
            self.access: set[str] = set()

    def check(self, msg: WxMsg, admin: str) -> bool:
        from_group: bool = msg.from_group()
        from_admin: bool = msg.sender == admin
        from_friend: bool = not (from_admin or from_group)
        source = [from_friend, from_group, from_admin]
        if all((
                self.enable,
                msg.type in self.msgtype,
                [i and j for (i, j) in zip(source, self.match)] == self.match,
                msg.sender in self.access or "ALL" in self.access
        )):
            return True
        return False

    def __hash__(self):
        return hash(self.name)


class Registry(object):
    def __init__(self):
        self._registry: set[ProcessMsgFunc] = set()
        self.mt: set[ProcessMsgFunc] = set()
        self.acync: set[ProcessMsgFunc] = set()

    def add(self, func: ProcessMsgFunc):
        self._registry.add(func)
        if func.mode == 'mt':
            self.mt.add(func)
        elif func.mode == 'async':
            self.acync.add(func)
        else:
            raise ValueError(f"Wrong startup method {func.mode}")

    def names(self):
        return [i.name for i in self._registry]

    async def process(self, msg: WxMsg) -> None:
        for f in self.mt:
            if f.check(msg):
                self.mt_executor.submit(f.func, msg)
        await asyncio.gather(*[f.func(msg) for f in self.acync])

    def __getitem__(self, name) -> Optional[ProcessMsgFunc]:
        if item := list(filter(lambda i: i.name == name, self._registry)):
            return item[0]
        else:
            return None

    def __iter__(self):
        return iter(self._registry)
