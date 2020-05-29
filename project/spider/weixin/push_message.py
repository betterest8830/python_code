#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Xu'

"""
微信推送好友消息
"""


import requests
from wxpy import Bot
from threading import Timer
from urllib import request

bot = Bot()
# linux执行登陆请调用下面的这句
# bot = Bot(console_qr=2,cache_path="botoo.pkl")


def get_news():

    """
    获取金山词霸每日一句，英文和翻译
    """
    url = 'http://open.iciba.com/dsapi/'
    r = requests.get(url)
    content = r.json()['content']
    note = r.json()['note']
    img = r.json()['fenxiang_img']
    request.urlretrieve(img, './IMG/tmp.jpg')
    return content, note


def send_news():
    try:
        contents = get_news()
        # 你朋友的微信名称，不是备注，也不是微信帐号。
        my_friend = bot.friends().search('朗月')[0]
        my_friend.send(contents[0])
        my_friend.send(contents[1])
        my_friend.send_image('./IMG/tmp.jpg')
        # 每86400秒（1天），发送1次
        t = Timer(40, send_news)
        t.start()
    except Exception as e:
        my_friend = bot.friends().search('独家记忆')[0]
        my_friend.send('今天消息发送失败！')
        pass


if __name__ == '__main__':
    send_news()
