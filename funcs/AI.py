# -*- coding: utf-8 -*-
# @Time    : 2023/12/17 14:16
# @Author  : 之落花--falling_flowers
# @File    : AI.py
# @Software: PyCharm
import json
import logging
import time
from abc import ABC, abstractmethod
from typing import Any, Callable
from typing import TypeVar

import google.api_core.exceptions
import google.generativeai as genai
import requests
import wcferry

from suswx import Configuration

_T = TypeVar('_T')


class _AI(ABC):
    """
    An AI that can be used for WeChat interaction
    """

    def __init__(self, wcf: wcferry.Wcf, config: Configuration, logger: logging.Logger) -> None:
        """
        :param wcf: your wcf instance
        :param config: your configuration of the AI
        :param logger: the logger instance
        """
        self._wcf: wcferry.Wcf = wcf
        self._config: Configuration = config
        self.__info: dict[str, Any] = {}
        self._logger: logging.Logger = logger
        self.name: str = "AI"
        self.key: str = ""

    @abstractmethod
    def private_reply(self, msg: wcferry.WxMsg) -> None:
        pass

    def _reply(
            self,
            msg: wcferry.WxMsg,
            get_default_info: Callable[[], _T],
    ) -> None:
        sender: str = msg.sender
        ai_name, ai_key = self.name, self.key
        config = self._config.__getattr__(ai_name.lower())
        if sender not in config["allow_list"] or not config["enable"]:
            return
        user_info: _T = self.__info.setdefault(sender, get_default_info())
        content: str = msg.content
        if content.startswith(ai_key + ai_name.lower()):
            self._wcf.send_text(user_info.command(content.split(" ")[-1]), sender)
            return
        if user_info.state or content.startswith(ai_key):
            if user_info.waiting:
                while user_info.waiting:
                    time.sleep(0.5)
            user_info.wait()
            self._get_ai_response(content, sender, user_info)
            user_info.wake()

    @abstractmethod
    def _get_ai_response(self, content: str, sender: str, user: "_T") -> None:
        pass

    class AIInfo(ABC):
        """
        Used to record AI's records of each session and answer user's command
        """

        def __init__(self) -> None:
            self.__waiting: bool = False
            self.__state: bool = False
            self.name: str = "AI"
            self.key: str = ""

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
            pass

        def _process_command(self, order: str, clear_func: Callable, help_docs: str) -> str:
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


class Gemini(_AI):
    """
    Used to record Gemini's records of each session and answer user's command
    """

    def __init__(self, wcf: wcferry.Wcf, config: Configuration, logger: logging.Logger) -> None:
        super().__init__(wcf, config, logger)
        self.name = "Gemini"
        self.key = "%"
        genai.configure(api_key=config.gemini['token'])
        self.__model: genai.GenerativeModel = genai.GenerativeModel('gemini-pro')

    def private_reply(self, msg: wcferry.WxMsg) -> None:
        """
        Methods for answering WeChat private messages by Gemini
        :param msg: Pending friend's message
        """
        self._reply(
            msg=msg,
            get_default_info=lambda: Gemini._GeminiInfo(self.__model),
        )

    def _get_ai_response(self, content: str, sender: str, user: "Gemini._GeminiInfo") -> None:
        try:
            response: genai.types.GenerateContentResponse = user.chat.send_message(
                content=content[int(not user.state):])
            self._wcf.send_text(resp := "[Gemini]%s" % response.text, sender)
            self._logger.info(resp)
        except google.api_core.exceptions.GoogleAPIError:
            self._wcf.send_text(resp := "Sorry, Gemini's answer timed out", sender)
            self._logger.info(resp)
        except google.generativeai.types.BlockedPromptException as e:
            self._wcf.send_text(resp := "Sorry, your prompt has been blocked", sender)
            self._logger.info(resp)
            self._logger.info(e)

    class _GeminiInfo(_AI.AIInfo):
        __Gemini_HELP: str = """Gemini command:
  %xxx 与Gemini对话
  %gemini help 获取帮助
  %gemini start 开启Gemini连续对话
  %gemini end 关闭Gemini连续对话
  %gemini clear 清空当前会话"""

        def __init__(self, model: genai.GenerativeModel) -> None:
            super().__init__()
            self.chat: genai.ChatSession = model.start_chat(history=[])
            self.name = "Gemini"
            self.key = "%"

        def command(self, order: str) -> str:
            return self._process_command(
                order=order,
                clear_func=self.chat.history.clear,
                help_docs=self.__Gemini_HELP
            )


class GPT(_AI):
    """
    A GPT that can be used for WeChat interaction
    """

    __URL: str = "http://w5.xjai.cc/api/chat-process"
    __SYSTEM_MESSAGE: str = "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown."
    __HEADERS: dict[str, str] = {
        "Host": "w5.xjai.cc",
        "Proxy-Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Origin": "http://w5.xjai.cc",
        "Referer": "http://w5.xjai.cc/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    def __init__(self, wcf: wcferry.Wcf, config: Configuration, logger: logging.Logger) -> None:
        super().__init__(wcf, config, logger)
        self.name: str = "GPT"
        self.key: str = "/"

    def private_reply(self, msg: wcferry.WxMsg) -> None:
        self._reply(
            msg=msg,
            get_default_info=GPT._GPTInfo
        )

    def _get_ai_response(self, content: str, sender: str, user: "_T") -> None:
        if response := self.__get_reply(content[int(not user.state):], user):
            user.pmid = response["id"]
            self._wcf.send_text(resp := "[GPT]%s" % response["text"], sender)
            self._logger.info(resp)
        else:
            self._wcf.send_text(resp := "Sorry, GPT's answer timed out", sender)
            self._logger.info(resp)

    def __get_reply(self, msg: str, info: "GPT._GPTInfo") -> dict | None:
        """
        Get GPT answer
        :param msg: content of message
        :param info: The wxid of the chat object
        :return: a tuple of pmid and response's text or None(ConnectionError or other)
        """
        try:
            response: dict[str, str] = json.loads(
                requests.post(
                    self.__URL,
                    headers=self.__HEADERS,
                    json={
                        "prompt": msg,
                        "options": {"parentMessageId": info.pmid} if info.pmid else {},
                        "systemMessage": self.__SYSTEM_MESSAGE,
                        "temperature": info.temperature,
                        "top_p": info.top_p,
                    },
                    timeout=20,
                ).text.split("&KFw6loC9Qvy&")[-1]
            )
            return {"id": response["id"], "text": response["text"]}
        except requests.exceptions.RequestException:
            return None

    class _GPTInfo(_AI.AIInfo):
        """
        Used to record GPT's records of each session and answer user's command
        """
        __GPT_HELP: str = """gpt command:
  /xxx 与gpt对话
  /gpt help 获取帮助
  /gpt start 开启gpt连续对话
  /gpt end 关闭gpt连续对话
  /gpt clear 清空当前会话"""

        def __init__(self):
            super().__init__()
            self.__top_p: float = 1.0
            self.__temperature: float = 0.8
            self.pmid: str = ""
            self.name: str = "GPT"
            self.key: str = "/"

        def clear(self):
            self.pmid = ""

        def command(self, order: str) -> str:
            return self._process_command(
                order=order,
                clear_func=self.clear,
                help_docs=self.__GPT_HELP
            )

        @property
        def top_p(self) -> float:
            """
            User's top_p (between 0 and 1)
            """
            return self.__top_p

        @property
        def temperature(self) -> float:
            """
            User's temperature (between 0 and 2)
            """
            return self.__temperature
