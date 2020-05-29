#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Xu'

"""
爬虫百度贴吧
"""

import re
import codecs
import traceback

import requests
from lxml import etree

import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)-8s %(message)s')

# user_agent = 'Mozilla/5.0 (Linux; U; Android 4.4.4; Nexus 5 Build/KTU84P)
# AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
user_agent = 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.04'
headers = {'User-Agent': user_agent}


# 处理页面标签类
class Tool(object):
    # 去除img标签,7位长空格
    remove_img = re.compile('<img.*?>| {7}')  # 行后注释
    # 删除超链接
    remove_addr = re.compile('<a.*?>|</a>')
    # 将换行符或者双换行符替换\n
    replace_br = re.compile('<br>|<br><br>')
    # 把换行的标签换为\n
    replace_line = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replace_td = re.compile('<td>')
    # 把段落开头换为\n加空两格
    replace_para = re.compile('<p.*?>')
    # 将其余标签剔除
    remove_extra_tag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.remove_img, '', x)
        x = re.sub(self.remove_addr, '', x)
        x = re.sub(self.replace_br, '\n', x)
        x = re.sub(self.replace_line, '\n', x)
        x = re.sub(self.replace_td, '\t', x)
        x = re.sub(self.replace_para, '\n    ', x)
        x = re.sub(self.remove_extra_tag, '', x)

        return x.strip()


# 百度贴吧爬虫类
class BaiDuTieBa(object):
    """百度贴吧类

    爬虫百度贴吧

    Attributes:
        base_url (str): 基本url
        see_lz (int): 是否只看楼主
    """

    # https://tieba.baidu.com/p/3138733512?see_lz=1&pn=4
    def __init__(self, base_url, see_lz, floor_tag):
        # base 链接地址
        self.base_url = base_url
        # 是否看楼主
        self.see_lz = '?see_lz=' + str(see_lz)
        # HTML标签剔除工具类对象
        self.tool = Tool()
        # 全局file变量，文件写入操作对象
        self.file = None
        # 楼层标号，初始为1
        self.floor = 1
        # 默认的标题，如果没有成功获取到标题的话则会用这个标题
        self.default_title = '百度贴吧'
        # 是否写入楼分隔符的标记
        self.floor_tag = floor_tag

    # 输入页码，获得该页码的代码
    def get_page(self, page_num):
        try:
            url = self.base_url + self.see_lz + '&pn=' + str(page_num)
            # 添加错误的headers会出现问题
            r = requests.get(url, headers=headers, timeout=5)
            return r.content.decode('utf-8')
        except Exception as e:
            logging.error('Spider Failure!')

    # 获得帖子标题
    def get_title(self, page):
        """获取帖子标题

        如果没有标题可以获取默认标题

        Args:
            page (str): 主页html

        Returns:
            帖子题目

        Raises:
             pass

        Examples:
            >>> google = GoogleStyle(divisor=10)
            >>> google.divide(10)
            1.0

        References:
            pass
        """
        tree = etree.HTML(page)
        title = tree.xpath('//h3/text()')[0].strip()
        return title

    # 获得帖子一共多少页
    def get_page_num(self, page):
        tree = etree.HTML(page)
        page_num = tree.xpath('//div[@class="pb_footer"]//span[@class="red"][2]/text()')[0].strip()

        return page_num

    # 解析代码获得帖子内容
    def get_content(self, page):
        pat = re.compile(r'<div id="post_content.*?>(.*?)</div>', re.S)
        items = re.findall(pat, page)
        contents = []

        for item in items:
            content = '\n' + self.tool.replace(item)
            contents.append(content)

        return contents

    def set_file_title(self, title):
        if title:
            self.file = codecs.open('./data/bdtb/' + title + '.txt', 'w+', encoding='utf-8')
        else:
            self.file = codecs.open('./data/bdtb/' + self.default_title + '.txt', 'w+', encoding='utf-8')

    def write_data(self, contents):
        for item in contents:
            # 楼层分隔符
            if self.floor_tag == '1':
                floor_line = '\n\n' '-----第' + str(self.floor) + '楼-----' + '\n'
                self.file.write(floor_line)
            self.file.write(item)
            self.floor += 1

    def start(self):
        index_page = self.get_page(1)
        page_num = self.get_page_num(index_page)
        title = self.get_title(index_page)
        self.set_file_title(title)

        if page_num is None:
            logging.error('URL已经失效！')
            return
        try:
            logging.info('该帖子共有' + str(page_num) + '页')
            for i in range(1, int(page_num) + 1):
                logging.info('正在写入第' + str(i) + '页数据')
                page = self.get_page(i)
                contents = self.get_content(page)
                self.write_data(contents)
        except IOError:
            logging.error('写入异常，原因：' + traceback.format_exc())
        finally:
            logging.info('写入任务完成！')


def main():
    # tiezi_code = '3138733512'
    tiezi_code = '5609507239'
    base_url = 'http://tieba.baidu.com/p/' + str(tiezi_code)
    see_lz, floor_tag = '1', '1'
    bdtb = BaiDuTieBa(base_url, see_lz, floor_tag)
    bdtb.start()


def test():
    print('请输入梯子代号')
    base_url = 'http://tieba.baidu.com/p/' + str(input('http://tieba.baidu.com/p/'))
    see_lz = input('是否只获取楼主发言，是输入1，否输入0\n')
    floor_tag = input('是否写入楼层信息，是输入1，否输入0\n')
    bdtb = BaiDuTieBa(base_url, see_lz, floor_tag)
    bdtb.start()


if __name__ == '__main__':
    main()
