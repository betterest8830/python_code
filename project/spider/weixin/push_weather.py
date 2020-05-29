#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Xu'

"""
微信推送群天气情况
"""

import datetime
from threading import Timer

from wxpy import *
import requests
from lxml import etree

ua = 'Mozilla/5.0 (Linux; U; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
headers = {'User-Agent': ua}

bot = Bot()
g_cities = ['baiquan', 'beijing', 'jiujiang']


# 每天定时运行
def main_run():
    now_time = datetime.datetime.now()
    next_time = now_time + datetime.timedelta(days=+1)
    next_year = next_time.date().year
    next_month = next_time.date().month
    next_day = next_time.date().day
    next_time = datetime.datetime.strptime(str(next_year)+"-" +
                                           str(next_month)+"-"+str(next_day)+" 8:00:00", "%Y-%m-%d %H:%M:%S")
    timer_start_time = (next_time - now_time).total_seconds()
    timer = Timer(timer_start_time, send_weather)
    timer.start()


# 获取天气情况
def get_weather():
    res_l = []
    for city in g_cities:
        url = 'https://www.tianqi.com/%s/' % city
        r = requests.get(url, headers=headers, timeout=5)
        tree = etree.HTML(r.content.decode('utf-8'))
        week = tree.xpath('//dd[@class="week"]/text()')[0].strip()
        weather = tree.xpath('//dd[@class="weather"]/span/b/text()')[0].strip()
        temperature = tree.xpath('//dd[@class="weather"]/span/text()')[0].strip()
        wind = tree.xpath('substring-after(//dd[@class="shidu"]/b[2]/text(), "：")')
        wind = ''.join(wind).strip()
        kongqi = tree.xpath('substring-after(//dd[@class="kongqi"]/h5/text(), "：")')[0].strip()
        # city_l = ['日历: ' + week, '天气: ' + weather, '温度: ' + temperature, '风向: ' + wind, '空气质量: ' + kongqi]
        city_l = ['城市:' + city, '天气: ' + weather, '温度: ' + temperature, '风向: ' + wind, '空气质量: ' + kongqi]
        city_str = '\n'.join(city_l)
        res_l.append(city_str)

    return res_l


# 发送天气
def send_weather():
    try:
        res_l = get_weather()
        my_friend = bot.groups().search('测试群')[0]
        my_friend.send(res_l[0])
        my_friend.send(res_l[1])
        my_friend.send(res_l[2])
        t = Timer(60, send_weather)
        t.start()
    except Exception as e:
        print(e)
        my_friend = bot.friends().search('独家记忆')[0]
        my_friend.send(u"今天消息发送失败了")


if __name__ == '__main__':
    # get_weather()
    send_weather()
    #main_run()