# -*- coding: utf-8 -*-
# @Time    : 2023/12/16 17:13
# @Author  : 之落花--falling_flowers
# @File    : Gemini.py
# @Software: PyCharm
import logging
import time

import google.api_core.exceptions
import google.generativeai as genai
import wcferry

from suswx import Configuration


class Gemini(object):
    """
    A Gemini that can be used for WeChat interaction
    """

    def __init__(self, wcf: wcferry.Wcf, config: Configuration, logger: logging.Logger) -> None:
        """
        :param wcf: your wcf instance
        :param config: your configuration of Gemini
        :param logger: the logger instance
        """
        self.__wcf: wcferry.Wcf = wcf
        self.__config: Configuration = config.gemini
        self.__model: genai.GenerativeModel = genai.GenerativeModel('gemini-pro')
        self.__info: dict[str, Gemini._GeminiInfo] = {}
        self.__logger: logging.Logger = logger
        genai.configure(api_key=config.gemini['token'])

    def private_reply(self, msg: wcferry.WxMsg) -> None:
        """
        Methods for answering WeChat private messages by Gemini
        :param msg: Pending friend's message
        """
        sender: str = msg.sender
        if sender not in self.__config["allow_list"] or not self.__config["enable"]:
            return
        user: Gemini._GeminiInfo = self.__info.setdefault(sender, Gemini._GeminiInfo(self.__model))
        content: str = msg.content
        if content.startswith("%gemini"):
            self.__wcf.send_text(user.command(content.split(" ")[-1]), sender)
            return
        if user.state or content.startswith("%"):
            if user.waiting:
                while user.waiting:
                    time.sleep(0.5)
            user.wait()
            try:
                response: genai.types.GenerateContentResponse = user.chat.send_message(
                    content=content[int(not user.state):])
                self.__wcf.send_text(resp := "[Gemini]%s" % response.text, sender)
                self.__logger.info(resp)
            except google.api_core.exceptions.GoogleAPIError:
                self.__wcf.send_text(resp := "Sorry, Gemini's answer timed out", sender)
                self.__logger.info(resp)
            except google.generativeai.types.BlockedPromptException as e:
                self.__wcf.send_text(resp := "Sorry, your prompt has been blocked", sender)
                self.__logger.info(resp)
                self.__logger.info(e)
            user.wake()

    class _GeminiInfo(object):
        """
        Used to record Gemini's records of each session and answer user's command
        """

        __Gemini_HELP: str = """Gemini command:
  %xxx 与Gemini对话
  %gemini help 获取帮助
  %gemini start 开启Gemini连续对话
  %gemini end 关闭Gemini连续对话
  %gemini clear 清空当前会话"""

        def __init__(self, model: genai.GenerativeModel) -> None:
            self.__waiting: bool = False
            self.__state: bool = False
            self.chat: genai.ChatSession = model.start_chat(history=[])

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

        def command(self, order: str) -> str:
            """
            Reply to user's Gemini command and Change user's info
            :param order: User command content
            :return: Contents of reply command
            """
            match order:
                case "start":
                    self.__state = True
                    return "Gemini has been turned on"
                case "end":
                    self.__state = False
                    return "Gemini has been turned off"
                case "clear":
                    self.chat.history.clear()
                    return "Gemini has been cleared memory"
                case "help":
                    return self.__Gemini_HELP
                case _:
                    return '指令错误,可发送"%gemini help"获取帮助'
