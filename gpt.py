# -*- coding: utf-8 -*-
# @Time    : 2023/12/9 22:31
# @Author  : 之落花--falling_flowers
# @File    : gpt.py
# @Software: PyCharm
import json

import requests

systemMessage = "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown."


class GPT(object):
    def __init__(self) -> None:
        self.__url: str = "http://w5.xjai.cc/api/chat-process"
        self.__headers: dict = {
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
        self.__temperature: float = 0.8
        self.__top_p: float = 1.0
        self.__pmid: str = ""

    def __call__(self, msg: str) -> str:
        response = json.loads(
            requests.post(
                self.__url,
                headers=self.__headers,
                json={
                    "prompt": msg,
                    "options": {"parentMessageId": self.__pmid} if self.__top_p else {},
                    "systemMessage": systemMessage,
                    "temperature": self.__temperature,
                    "topP": self.__top_p,
                },
            ).text.split("&KFw6loC9Qvy&")[-1]
        )
        self.__pmid = response["id"]
        return response["text"]


def main():
    gpt = GPT()
    while True:
        prompt = input()
        if not prompt:
            continue
        if prompt == "quit":
            break
        resp = gpt(prompt)
        print(resp)


if __name__ == "__main__":
    main()
