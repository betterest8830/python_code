# coding=utf8

import codecs
import datetime
import time
import functools
import hashlib

# 1、python 中的open函数
# Python3直接用open。Python2.x下用codecs.open, 读取的都是字符串类型
# python2 的open,读取的是str类型
def read1():
    input_file = 'data/input1.txt'
    with open(input_file, 'r', encoding='utf8') as f:
        for line in f.readlines():
            print(type(line), line)
            line = line.encode('utf8')
            print(type(line), line)
#read1()
def read2():
    input_file = 'data/input1.txt'
    with open(input_file, 'r', encoding='utf8') as f:
        line = f.readline()
        while line:
            print(line)
            line = f.readline()
#read2()


# 2、python 如何替代python2 中的cmp
b = ['1', '5', '21', '4']
cmp=lambda x, y: -1 if x+y < y+x else 1
print(sorted(b, key=functools.cmp_to_key(cmp)))


# 3、时间转换
s = 'Tue Aug 25 18:10:36 2020'
s = time.strptime(s, "%a %b %d %H:%M:%S %Y")
print(s)
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


# 4、md5算法
def curlmd5(src):
    m = hashlib.md5()
    m.update(src.encode('UTF-8'))
    return m.hexdigest()
print(curlmd5('sogounovel'))


t = tuple('123')
print(t)
print(int(12.34))
print(int(-12.34))