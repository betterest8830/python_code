#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Xu'

"""
访问CSDN
"""

import random
import time

import requests

import sys
# 在终端执行需要添加路径
# sys.path.append(r'C:\Users\xuchunlong\Desktop\python35_study\project')

g_user_agent_list = [
    'Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0)',
    'Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.0;Trident/4.0)',
    'Mozilla/4.0(compatible;MSIE7.0;WindowsNT6.0)',
    'Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11',
    'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',
]

g_url_list1 = [
    'https://blog.csdn.net/pushup8/article/details/85071735',
    'https://blog.csdn.net/pushup8/article/details/85013445',
    'https://blog.csdn.net/pushup8/article/details/85196465',
    'https://blog.csdn.net/pushup8/article/details/85200248',
    'https://blog.csdn.net/pushup8/article/details/85268115',
    'https://blog.csdn.net/pushup8/article/details/85268115',
    'https://blog.csdn.net/pushup8/article/details/85341207',
    'https://blog.csdn.net/pushup8/article/details/85342586',
    'https://blog.csdn.net/pushup8/article/details/85757763',
    'https://blog.csdn.net/pushup8/article/details/86014556',
    'https://blog.csdn.net/pushup8/article/details/86014556',
    'https://blog.csdn.net/pushup8/article/details/86020862',
]

g_url_list = [
    'https://www.jianshu.com/p/c9bf41433510',
    'https://www.jianshu.com/p/deba36e576c2',
    'https://blog.csdn.net/pushup8/article/details/86014556',
    'https://blog.csdn.net/pushup8/article/details/86020862',
]


def get_proxies():
    # 公司的代理，如果没有的话，使用西刺代理
    index = random.randint(1, 48)
    proxies = {
        "http": "http://adslspider%02d.web.zw.ted:9090" % index,
        "https": "http://adslspider%02d.web.zw.ted:9090" % index,
    }
    return proxies


def visit_csdn():
    total_num = 0
    headers = {'Uset-Agent': random.choice(g_user_agent_list),}
    while True:
        url = random.choice(g_url_list)
        try:
            r = requests.get(url, headers=headers, timeout=5)
        except Exception:
            print('代理出现问题')
            time.sleep(random.random() * 10)
        else:
            print('已经刷了 %s 次' % (total_num))
            time.sleep(12 + random.random() * 10)
            total_num += 1
            if total_num % 17 == 0:
                time.sleep(60 + random.random() * 6)


if __name__ == '__main__':
    visit_csdn()