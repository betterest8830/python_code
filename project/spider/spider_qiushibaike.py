#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Xu'

"""
爬虫糗事百科
"""

import requests
from lxml import etree

import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)-8s %(message)s')

# user_agent = 'Mozilla/5.0 (Linux; U; Android 4.4.4; Nexus 5 Build/KTU84P)
# AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
user_agent = 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.04'
headers = {'User-Agent': user_agent}


# 糗事百科爬虫类
class QiuShiBaiKe(object):

    def __init__(self):
        self.page_index = 1
        self.stories = []
        # 存放程序是否继续运行的变量
        self.enable = False

    # 传入某一页的索引获得页面代码
    def get_page(self, page_index):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(page_index)
            r = requests.get(url, headers=headers, timeout=5)
            return r.content.decode('utf-8')
        except Exception as e:
            print('Spider Failure!')
            return

    def get_page_items(self, page_index):
        content = self.get_page(page_index)
        tree = etree.HTML(content)
        contents = []
        items = tree.xpath('//div[@class="content"]')
        for item in items:
            tmp_l = item.xpath('./span/text()')
            tmp_str = '\n'.join(tmp_l).strip()
            contents.append(tmp_str)
        names = [x.strip() for x in tree.xpath('//h2/text()')]
        page_stories = [[x, y] for x, y in zip(names, contents)]

        return page_stories

    def load_page(self):
        if self.enable:
            if len(self.stories) < 2:
                page_stories = self.get_page_items(self.page_index)
                if page_stories:
                    self.stories.append(page_stories)
                    self.page_index += 1

    def ge_one_story(self, page_stories, page):
        for story in page_stories:
            tmp = input()
            self.load_page()
            if tmp == 'Q':
                self.enable = False
                return
            print('第%s页\t发布人：%s\n%s' % (page, story[0], story[1]))

    def start(self):
        print('正在读取糗事百科，按回车键查询新段子，Q退出')
        self.enable = True
        self.load_page()

        now_page = 0
        while self.enable:
            if len(self.stories) > 0:
                page_stories = self.stories[0]
                now_page += 1
                del self.stories[0]
                self.ge_one_story(page_stories, now_page)


def main():
    spider = QiuShiBaiKe()
    spider.start()


def test(index=1):
    url = 'https://www.qiushibaike.com/hot/page/' + str(index)
    try:
        r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status()
    except Exception as e:
        print('Spider Failure!')
    else:
        print('Spider Success!')

    contents = []
    tree = etree.HTML(r.content.decode('utf-8'))
    items = tree.xpath('//div[@class="content"]')
    for item in items:
        tmp_l = item.xpath('./span/text()')
        tmp_str = '\n'.join(tmp_l).strip() + '\n'
        print(tmp_str)
        contents.append(tmp_str)
        print(len(contents))
    names = [x.strip() for x in tree.xpath('//h2/text()')]
    print(names)


if __name__ == '__main__':
    # test(1)
    main()
