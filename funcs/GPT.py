# -*- coding: utf-8 -*-
# @Time    : 2023/12/9 22:31
# @Author  : 之落花--falling_flowers
# @File    : GPT.py
# @Software: PyCharm
import json
import logging
import time

import requests
import wcferry

from suswx import Configuration


class GPT(object):
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

    def __init__(
            self, wcf: wcferry.Wcf, config: Configuration, logger: logging.Logger
    ) -> None:
        """
        :param wcf: your wcf instance
        :param config: your configuration of gpt
        """
        self.__wcf: wcferry.Wcf = wcf
        self.__config: Configuration = config.gpt
        self.__info: dict[str, GPT._GPTInfo] = {}
        self.__logger: logging.Logger = logger

    def private_reply(self, msg: wcferry.WxMsg) -> None:
        """
        Methods for answering WeChat private messages by GPT
        :param msg: Pending friend's message
        """
        sender: str = msg.sender
        if sender not in self.__config["allow_list"] or not self.__config["enable"]:
            return
        user: GPT._GPTInfo = self.__info.setdefault(sender, GPT._GPTInfo())
        content: str = msg.content
        if content.startswith("/gpt"):
            self.__wcf.send_text(user.command(content.split(" ")[-1]), sender)
            return
        if user.state or content.startswith("/"):
            if user.waiting:
                while user.waiting:
                    time.sleep(0.5)
            user.wait()
            if response := self.__reply(content[int(not user.state):], user):
                user.pmid = response["id"]
                self.__wcf.send_text(resp := "[GPT]%s" % response["text"], sender)
                self.__logger.info(resp)
            else:
                self.__wcf.send_text(resp := "Sorry, my answer timed out", sender)
                self.__logger.info(resp)
            user.wake()

    def __reply(self, msg: str, info: "GPT._GPTInfo") -> dict | None:
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
                    timeout=10,
                ).text.split("&KFw6loC9Qvy&")[-1]
            )
            return {"id": response["id"], "text": response["text"]}
        except requests.exceptions.RequestException:
            return None

    class _GPTInfo(object):
        """
        Used to record GPT's records of each session and answer user's command
        """

        __GPT_HELP: str = """gpt command:
  /xxx 与gpt对话
  /gpt help 获取帮助
  /gpt start 开启gpt连续对话
  /gpt end 关闭gpt连续对话
  /gpt clear 清空当前会话"""

        def __init__(self) -> None:
            self.__waiting: bool = False
            self.__state: bool = False
            self.__top_p: float = 1.0
            self.__temperature: float = 0.8
            self.pmid: str = ""

        @property
        def waiting(self) -> bool:
            """
            Whether the user is waiting for a reply
            """
            return self.__waiting

        @property
        def state(self) -> bool:
            """
            Whether the user has enabled GPT continuous conversations
            """
            return self.__state

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

        @top_p.setter
        def top_p(self, value: float) -> None:
            if value < 0 or value > 1:
                raise ValueError("You must enter a number between 0 and 1")
            else:
                self.__top_p = value

        @temperature.setter
        def temperature(self, value: float) -> None:
            if value < 0 or value > 2:
                raise ValueError("You must enter a number between 0 and 2")
            else:
                self.__temperature = value

        def command(self, order: str) -> str:
            """
            Reply to user's gpt command and Change user's info
            :param order: User command content
            :return: Contents of reply command
            """
            match order:
                case "start":
                    self.__state = True
                    return "ChatGPT has been turned on"
                case "end":
                    self.__state = False
                    return "ChatGPT has been turned off"
                case "clear":
                    self.pmid = ""
                    return "ChatGPT has been cleared memory"
                case "help":
                    return self.__GPT_HELP
                case _:
                    return '指令错误,可发送"/gpt help"获取帮助'
