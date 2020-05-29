#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from wxpy import Bot
from wxpy import embed

# 去图灵机器人官网注册后会生成一个apikey，可在个人中心查看
KEY = 'eecb361a41c44f7fb7a95013d0b6efd9'
root = Bot()


def talk_robot(info='你好啊'):
    api_url = 'http://www.tuling123.com/openapi/api'
    apikey = KEY
    data = {'key': apikey, 'info': info}
    r = requests.post(api_url, data=data)
    response = r.json()['text']
    print(response)
    return response


@root.register()
def reply_my_friend(msg):
    message = '{}'.format(msg.text)
    response = talk_robot(info=message)
    return response


#  embed() 方法就可以让程序保持运行
embed()