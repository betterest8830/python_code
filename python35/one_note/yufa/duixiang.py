#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy


# 浅拷贝
def test_1():
    a = [1, 2]
    b = list(a)
    print(id(a), id(b))
    for x, y in zip(a, b):
        print(id(x), id(y))
    '''
    2337731000072 2337739881800
    1648230864 1648230864
    1648230896 1648230896
    '''


# 深拷贝
def test_2():
    a = [1, 2]
    b = copy.deepcopy(a)
    print(id(a), id(b))
    for x, y in zip(a, b):
        print(id(x), id(y))
    '''
    # 为什么使用了深拷贝，a和b中元素的id还是一样呢？
    2458513957384 2458505197320
    1648230864 1648230864
    1648230896 1648230896
    '''


# 用一个包含可变对象的列表来确切地展示“浅拷贝”与“深拷贝”的区别
def test_3():
    a = [[1, 2], [5, 6]]
    b = copy.copy(a)
    c = copy.deepcopy(a)
    print(id(a), id(b))  # a 和 b 不同
    for x, y in zip(a, b):  # a 和 b 的子对象相同
        print(id(x), id(y))
    '''
    2749379509640 2749379507464
    2749379428104 2749379428104
    2749379426184 2749379426184
    '''
    print(id(a), id(c))  # a 和 c 不同
    for x, y in zip(a, c):  # a 和 c 的子对象也不同
        print(id(x), id(y))
    '''
    2749379509640 2749370611528
    2749379428104 2749379437064
    2749379426184 2749379437128
    '''

test_1()
test_2()
test_3()