#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time
import codecs
import pandas as pd
import HTMLParser
import cgi


'''
# 1、全角转化为半角
# 2、时间转换
# 3、表格转换为文本
# 4、html转码问题
'''

# 1、全角转化为半角
def quan_to_ban(ustring):
    """全角转半角"""
    rstring = ''
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif 65374 >= inside_code >= 65281:  # 全角字符（除空格）根据关系转化
            inside_code -= 65248
        rstring += unichr(inside_code)
    return rstring
def test_01():
    b = quan_to_ban(u'１７３３２３２４１８７６６５５０６６６０')
    print b.encode('utf8')


# 2、时间转换
# 时间戳转化为字符串
def timestamp_to_format(timestamp):
    struct_time = time.gmtime(timestamp)
    format_time = time.strftime("%Y-%m-%d %X", struct_time)
    return format_time
# 字符串转化为时间戳
def format_to_timestamp(format_time):
    struct_time = time.strptime(format_time, "%Y-%m-%d %X")
    timestamp = time.mktime(struct_time)
    return timestamp
def test_02():
    print 'timestamp:', time.time()
    print 'struct_time:', time.localtime(time.time())
    format_time = timestamp_to_format(time.time())
    print 'format_time:', format_time
    timestamp = format_to_timestamp(format_time)
    print 'timestamp:', timestamp


# 3、表格转换为文本
def xlsx_to_csv(xlsx_f, csv_f, csv_code='utf8'):
    # 指定第一列为索引列，不然默认增加一列数字
    xlsx_data = pd.read_excel(xlsx_f, index_col=0)
    xlsx_data.to_csv(csv_f, encoding=csv_code)
def csv_to_txt(xlsx_f, csv_f, txt_f, csv_code='utf8', txt_code='utf8'):
    xlsx_to_csv(xlsx_f, csv_f, csv_code)
    with codecs.open(txt_f, 'w', encoding=txt_code) as f:
        for line in file(csv_f):
            line = line.strip()
            if not line:
                continue
            row_l = line.decode(encoding=csv_code).split(',')
            if len(row_l) != 3:
                print row_l
                continue
            book_id, title, author = row_l[0], row_l[1], row_l[2]
            tmp = u'\t'.join([book_id, title, author]) + u'\n'
            f.write(tmp)
def test_03():
    f_xlsx = 'data/suixinkan0426.xlsx'
    f_csv = 'data/suixinkan0426.csv'
    f_txt = 'data/suixinkan0426.txt'
    csv_to_txt(f_xlsx, f_csv, f_txt)


# 4、html转码问题
def html_escape():
    # html转码问题
    html_str = '&lt;abc&gt;'
    html_parser = HTMLParser.HTMLParser()
    txt_str = html_parser.unescape(html_str)
    print(txt_str)  # 这样就得到了 txt_str = '<abc>'
    html_str = cgi.escape(txt_str)
    print(html_str)  # 这样又回到了 html_str = '&lt;abc&gt'


test_01()
test_02()
test_03()
html_escape()

