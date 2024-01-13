# -*- coding: utf-8 -*-
# @Time    : 2023/12/27 20:52
# @Author  : 之落花--falling_flowers
# @File    : Gemini.py
# @Software: PyCharm
import asyncio

import google.api_core.exceptions
import google.auth.exceptions
import google.generativeai as genai
from schema import Schema
from wcferry import WxMsg

from Configuration import config
from plugins import register
from plugins.AI.AI import AI
from suswx.bot import registry
from suswx.common import wcf, logger


class Gemini(AI):
    """
    A Gemini that can be used for WeChat interaction
    """

    def __init__(self) -> None:
        super().__init__("Gemini", "%")
        genai.configure(api_key=config["plugins"]["info"]["gemini"]["token"])
        self.__model: genai.GenerativeModel = genai.GenerativeModel('gemini-pro')

    async def private_reply(self, msg: WxMsg) -> None:
        """
        Methods for answering WeChat private messages by Gemini
        :param msg: Pending friend's message
        """
        await self._reply(msg=msg, get_default_info=lambda: Gemini._GeminiInfo(self.__model, self.name, self.key))

    async def _ai_response(self, content: str, sender: str, user_info: "Gemini._GeminiInfo") -> None:
        resp: str = "something wents wrong"
        try:
            response: genai.types.AsyncGenerateContentResponse = await asyncio.wait_for(
                user_info.chat.send_message_async(content=content[int(not user_info.state):]), 20)
            wcf.send_text(resp := "[Gemini]%s" % response.text, sender)
        except (google.api_core.exceptions.GoogleAPIError, asyncio.TimeoutError):
            wcf.send_text(resp := "Sorry, Gemini's answer timed out", sender)
        except (google.generativeai.types.BlockedPromptException,
                google.generativeai.types.generation_types.StopCandidateException) as e:
            wcf.send_text(resp := "Sorry, an exception occurs because of your prompt", sender)
            logger.info(e)
        except google.auth.exceptions.DefaultCredentialsError as e:
            resp = "Sorry, there may be an error in the gemini token, and the gemini function has been stopped."
            registry["gemini"].enable = False
            wcf.send_text(resp, sender)
            logger.info(e)
        finally:
            logger.info(resp)

    class _GeminiInfo(AI.AIInfo):
        """
        Used to record Gemini's records of each session and answer user's command
        """

        __Gemini_HELP: str = """Gemini command:
  %xxx 与Gemini对话
  %gemini help 获取帮助
  %gemini start 开启Gemini连续对话
  %gemini end 关闭Gemini连续对话
  %gemini clear 清空当前会话"""

        def __init__(self, model: genai.GenerativeModel, name: str, key: str) -> None:
            super().__init__(name, key)
            self.chat: genai.ChatSession = model.start_chat()

        def command(self, order: str) -> str:
            return self._process_command(
                order=order,
                clear_func=self.chat.history.clear,
                help_docs=self.__Gemini_HELP
            )


gemini_schma = Schema({"access": list, "enable": bool, "token": str})

if not gemini_schma.is_valid(config["plugins"]["info"]["gemini"]):
    config["plugins"]["info"]["gemini"]["token"] = ""
    config.save_config()

gemini_instance = Gemini()


@register(fromFriend=True, enable=False, mode="async")
async def gemini(msg: WxMsg) -> None:
    await gemini_instance.private_reply(msg)
