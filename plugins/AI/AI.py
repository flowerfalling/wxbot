# -*- coding: utf-8 -*-
# @Time    : 2023/12/17 14:16
# @Author  : 之落花--falling_flowers
# @File    : AI.py
# @Software: PyCharm
import asyncio
from abc import ABC, abstractmethod
from typing import Any, Callable
from typing import TypeVar

import wcferry

from suswx.common import wcf

T: type = TypeVar('T', bound="AI.AIInfo")

__all__ = ["AI", "Gemini", "GPT"]


class AI(ABC):
    """
    An AI that can be used for WeChat interaction
    """

    def __init__(self, name: str, key: str) -> None:
        """
        :param name: AI's name
        :param key: AI's identification symbol
        """
        self.__info: dict[str, Any] = {}
        self.name: str = name
        self.key: str = key

    @abstractmethod
    async def private_reply(self, msg: wcferry.WxMsg) -> None:
        """
        Function to reply to private message
        :param msg: 要处理的消息
        """
        ...

    async def _reply(
            self,
            msg: wcferry.WxMsg,
            get_default_info: Callable[[], T],
    ) -> None:
        sender: str = msg.sender
        ai_name, ai_key = self.name, self.key
        user_info: T = self.__info.setdefault(sender, get_default_info())
        content: str = msg.content
        if content.startswith(ai_key + ai_name.lower()):
            wcf.send_text(user_info.command(content.split(" ")[-1]), sender)
            return
        if user_info.state or content.startswith(ai_key):
            if user_info.waiting:
                while user_info.waiting:
                    await asyncio.sleep(0.5)
            user_info.wait()
            await self._ai_response(content, sender, user_info)
            user_info.wake()

    @abstractmethod
    async def _ai_response(self, content: str, sender: str, user_info: "T") -> None:
        """
        Function to get AI's reply
        :param content: Message content
        :param sender: sender's wxid
        :param user_info: sender's info
        """

    class AIInfo(ABC):
        """
        Used to record AI's records of each session and answer user's command
        """

        def __init__(self, name: str, key: str) -> None:
            self.__waiting: bool = False
            self.__state: bool = False
            self.name: str = name
            self.key: str = key

        @property
        def waiting(self) -> bool:
            """
            Whether the user is waiting for a reply
            """
            return self.__waiting

        @property
        def state(self) -> bool:
            """
            Whether the user has enabled continuous dialogue with AI
            """
            return self.__state

        def wait(self) -> None:
            """
            Set the user's wait status to Wait
            """
            self.__waiting = True

        def wake(self) -> None:
            """
            Set the user's wait status to Wake
            """
            self.__waiting = False

        @abstractmethod
        def command(self, order: str) -> str:
            """
            Used to process user commands for AI
            :param order: the user's command content
            """
            ...

        def _process_command(self, order: str, clear_func: Callable, help_docs: str) -> str:
            """
            Several methods for handling user commands to AI by default
            :param order: the user's command content
            :param clear_func: function to clear AI's memory
            :param help_docs: AI's help documentation
            :return:
            """
            match order:
                case "start":
                    self.__state = True
                    return f"{self.name} has been turned on"
                case "end":
                    self.__state = False
                    return f"{self.name} has been turned off"
                case "clear":
                    clear_func()
                    return f"{self.name} has been cleared memory"
                case "help":
                    return help_docs
                case _:
                    return f'指令错误,可发送"{self.key}{self.name.lower()} help"获取帮助'
