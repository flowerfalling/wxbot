# -*- coding: utf-8 -*-
# @Time    : 2023/12/9 22:16
# @Author  : 之落花--falling_flowers
# @File    : demo.py
# @Software: PyCharm
import queue
import time

from wcferry import Wcf

from gpt import GPT
from Middleware import Middleware

users = ['\u3000\u3000', 'Yang', 'ablaze']


def main():
    wcf = Wcf(debug=True)
    middleware = Middleware(wcf.get_friends())
    for user_name in users:
        for c in middleware.search_with_name(user_name):
            GPT().attach(c)
    while wcf.enable_receiving_msg():
        time.sleep(0.5)
        try:
            msg = wcf.get_msg()
            sender = middleware.search_with_wxid(msg.sender)
            if sender is None:
                continue
            if sender.info.name in users and msg.is_text():
                if (content := msg.content)[0] == '/':
                    resp = f'GPT:{sender.gpt.send(content[1:])}'
                    wcf.send_text(resp, sender.info.wxid)
                    print(f'<-{sender.info.name}\t|{content}')
                    print(f'->{sender.info.name}\t|{resp}')
        except queue.Empty:
            continue


if __name__ == '__main__':
    main()
