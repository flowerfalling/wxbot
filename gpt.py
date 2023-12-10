# -*- coding: utf-8 -*-
# @Time    : 2023/12/9 22:31
# @Author  : 之落花--falling_flowers
# @File    : gpt.py
# @Software: PyCharm
import json

import requests

systemMessage = "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown."


class GPT(object):
    def __init__(self):
        self.url = 'http://w5.xjai.cc/api/chat-process'
        self.headers = {
            'Host': 'w5.xjai.cc',
            'Proxy-Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Content-Type': 'application/json',
            'Origin': 'http://w5.xjai.cc',
            'Referer': 'http://w5.xjai.cc/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.temperature = 0.8
        self.top_p = 1.0
        self.pmid = ''

    def send(self, msg):
        data = '"prompt":"{}","options":{},"systemMessage":"{}","temperature":{:3},"top_p":{:3}'.format(
            msg, '{%s}' % f'"parentMessageID": "{self.pmid}"' if self.pmid else '{}', systemMessage, self.temperature,
            self.top_p
        )
        data = '{%s}' % data
        response = requests.request(
            method='post',
            url=self.url,
            headers=self.headers,
            data=data + '  ' * 30
        )
        json_response = json.loads(response.text.split('&KFw6loC9Qvy&')[-1])
        self.pmid = json_response['id']
        return json_response['text']

    def attach(self, chat):
        chat.gpt = self


def main():
    gpt = GPT()
    while True:
        prompt = input()
        if prompt == 'quit':
            break
        resp = gpt.send(prompt)
        print(resp)


if __name__ == '__main__':
    main()
