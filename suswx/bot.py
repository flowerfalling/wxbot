# -*- coding: utf-8 -*-
# @Time    : 2023/12/12 21:43
# @Author  : 之落花--falling_flowers
# @File    : bot.py
# @Software: PyCharm
import atexit
import queue
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Optional
from threading import Thread

from wcferry import WxMsg

from suswx import Content, Registry, ProcessMsgFunc
from suswx.common import wcf, logger, Admin, botadmin
from suswx.Registry import func_startup_mode
import asyncio

__all__ = ["robot", "register", "registry"]

registry: Registry = Registry()
msgQ = queue.Queue()


def register(
        msgType: tuple[Content] = (Content.TEXT,),
        fromFriend: bool = False,
        fromGroup: bool = False,
        fromAdmin: bool = False,
        name: Optional[str] = None,
        mode: func_startup_mode = "mt",
        enable: bool = True,
        access: Optional[set] = None
) -> Callable[[Callable[[WxMsg], None]], ProcessMsgFunc]:
    def inner(func: Callable[[WxMsg], None]) -> ProcessMsgFunc:
        func_name = name if name is not None else func.__name__
        process_func = ProcessMsgFunc(func, func_name, msgType, fromFriend, fromGroup, fromAdmin, mode, enable, access)
        registry.add(process_func)
        return process_func

    return inner


class Robot(object):
    """
    A WeChat robot framework
    """

    def __init__(self) -> None:
        self._admin: Admin = botadmin
        self.interval: float = 0.5
        self.mt_executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=50)

    async def run(self) -> None:
        """
        Keep the bot running and processing information
        """
        wcf.enable_receiving_msg()
        while wcf.is_receiving_msg():
            await asyncio.sleep(self.interval)
            try:
                msg: WxMsg = wcf.get_msg(block=False)
                asyncio.run_coroutine_threadsafe(self.process(msg), asyncio.get_running_loop())
            except queue.Empty:
                continue

    async def process(self, msg: WxMsg) -> None:
        if not msg.from_group() and msg.is_text():
            logger.info("[%s]: %s", wcf.get_info_by_wxid(msg.sender)["name"], msg.content)
        for f in registry.mt:
            if f.check(msg, self._admin.wxid):
                self.mt_executor.submit(f.func, msg)
        await asyncio.gather(*[asyncio.create_task(f.func(msg)) for f in registry.acync if f.check(msg, self._admin.wxid)])


def robot(name: str = "SUSBOT") -> Robot:
    """
    Get a WeChat bot
    :param name: the bot's name
    :return: robot instance, wcferry instance, logger instance, admin's wxid
    """
    logger.name = name
    bot: Robot = Robot()
    atexit.register(wcf.cleanup)
    atexit.register(lambda: print("Quit done"))
    return bot
