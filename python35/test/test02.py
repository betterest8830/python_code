# coding=utf8

import codecs


# Python3直接用open。Python2.x下用codecs.open, 读取的都是字符串类型
# python2 的open,读取的是字节类型
def read1():
    input_file = 'data/input1.txt'
    with open(input_file, 'r', encoding='utf8') as f:
        for line in f.readlines():
            print(type(line), line)
            line = line.encode('utf8')
            print(type(line), line)
read1()


def read2():
    input_file = 'data/input1.txt'
    with open(input_file, 'r', encoding='utf8') as f:
        line = f.readline()
        while line:
            print(line)
            line = f.readline()
read2()











