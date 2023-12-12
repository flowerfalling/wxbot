# -*- coding: utf-8 -*-
# @Time    : 2023/12/9 22:16
# @Author  : 之落花--falling_flowers
# @File    : demo.py
# @Software: PyCharm
import queue
import time

from wcferry import Wcf

from Process import Process

users = ["\u3000\u3000", "Yang", "ablaze"]


def main():
    wcf = Wcf(debug=True)
    process = Process(wcf)
    while wcf.enable_receiving_msg():
        time.sleep(0.5)
        try:
            msg = wcf.get_msg()
            process.process(msg)
        except queue.Empty:
            continue


if __name__ == "__main__":
    main()
