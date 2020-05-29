#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itchat
import requests

KEY = 'eecb361a41c44f7fb7a95013d0b6efd9'


# 根据info信息回复相应内容
def talk_robot(info='你好啊'):
    api_url = 'http://www.tuling123.com/openapi/api'
    apikey = KEY
    data = {'key': apikey, 'info': info}
    r = requests.post(api_url, data=data)
    response = r.json()['text']
    return response


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def print_content(msg):
    # 在群里只有@才能回复
    if msg['isAt']:
        print(msg)
        default_replay = '机器人出现故障...'
        return default_replay or talk_robot(msg['Text'])


if __name__ == '__main__':
    # 热启动不用每次扫码
    itchat.auto_login(hotReload=True)
    itchat.run()



