# -*- coding: utf-8 -*-
# @Time    : 2023/12/27 20:52
# @Author  : 之落花--falling_flowers
# @File    : GPT.py
# @Software: PyCharm
import json
from typing import Optional

import requests
from wcferry import WxMsg

from plugins.AI.AI import AI
from suswx.bot import register
from suswx.common import wcf, logger


class GPT(AI):
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

    def __init__(self) -> None:
        super().__init__("GPT", "/")

    def private_reply(self, msg: WxMsg) -> None:
        """
        Methods for answering WeChat private messages by GPT
        :param msg: Pending friend's message
        """
        self._reply(msg=msg, get_default_info=lambda: GPT._GPTInfo(self.name, self.key))

    def _ai_response(self, content: str, sender: str, user_info: "GPT._GPTInfo") -> None:
        if response := self.__get_reply(content[int(not user_info.state):], user_info):
            user_info.pmid = response["id"]
            wcf.send_text(resp := "[GPT]%s" % response["text"], sender)
            logger.info(resp)
        else:
            wcf.send_text(resp := "Sorry, GPT's answer timed out", sender)
            logger.info(resp)

    def __get_reply(self, msg: str, info: "GPT._GPTInfo") -> Optional[dict]:
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

    class _GPTInfo(AI.AIInfo):
        """
        Used to record GPT's records of each session and answer user's command
        """

        __GPT_HELP: str = """gpt command:
  /xxx 与gpt对话
  /gpt help 获取帮助
  /gpt start 开启gpt连续对话
  /gpt end 关闭gpt连续对话
  /gpt clear 清空当前会话"""

        def __init__(self, name: str, key: str):
            super().__init__(name, key)
            self.top_p: float = 1.0
            self.temperature: float = 0.8
            self.pmid: str = ""

        def clear(self):
            """
            Clear gpt session history
            """
            self.pmid = ""

        def command(self, order: str) -> str:
            return self._process_command(
                order=order,
                clear_func=self.clear,
                help_docs=self.__GPT_HELP
            )


gpt = GPT()
register(fromFriend=True, name="gpt")(gpt.private_reply)
