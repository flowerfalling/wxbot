# -*- coding: utf-8 -*-
# @Time    : 2023/12/9 22:16
# @Author  : 之落花--falling_flowers
# @File    : demo.py
# @Software: PyCharm
import queue
import time

from wcferry import Wcf
from gpt import GPT


users = ['\u3000\u3000', 'Yang']


def main():
    wcf = Wcf(debug=True)
    friends = wcf.get_friends()
    gpt = GPT()
    while wcf.enable_receiving_msg():
        time.sleep(0.5)
        try:
            msg = wcf.get_msg()
            for i in friends:
                if i['wxid'] == msg.sender and i['name'] in users and msg.is_text():
                    if (content := msg.content)[0] == '/':
                        resp = f'GPT:{gpt.send(content[1:])}'
                        wcf.send_text(resp, msg.sender)
                        print(f'user-{content}')
                        print(resp)
        except queue.Empty:
            continue


if __name__ == '__main__':
    main()
