#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys


class Cat(object):
    def __init__(self, name):
        self.name = name
    def __del__(self):
        print('对象消亡')
def test_1():
    cat1 = Cat('XXX')
    print(sys.getrefcount(cat1))  # 2,引用计数+1，因为当前也正在使用
    cat2 = cat1
    cat3 = cat1
    print(id(cat1), id(cat1), id(cat1), sep=':::')
    print(sys.getrefcount(cat1))
    del cat2
    del cat3
    print(sys.getrefcount(cat1))
    del cat1
    print('end')
'''
2
2095397979024:::2095397979024:::2095397979024
4
2
对象消亡(这是结束才打印的，或者全部引用都删掉后引用)
end
'''

class A(object):
    def __init__(self):
        print('object born id:%s' % str(hex(id(self))))
def func(c):
    # getrefcount()方法用于返回对象的引用计数
    print('obejct refcount is: ', sys.getrefcount(c))  # 4，5，4
def test_2():
    a = A()
    func(a)
    print(sys.getrefcount(a))  # 2
    b = a
    func(a)
    del b
    func(a)


# test_1()
test_2()
