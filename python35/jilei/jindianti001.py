#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# 1、写出把str转换为int的函数：
from functools import reduce
def test_01():
    DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
    def char2num(c):
        return DIGITS[c]
    def str2int(s):
        return reduce(lambda x, y: x*10+y, map(char2num, s))
    print(str2int('2345'))


# 2、计算素数的一个方法是埃氏筛法
def test_02():
    def _odd_iter():
        n = 1
        while True:
            n = n + 2
            yield n
    def _not_divisible(n):
        return lambda x: x % n > 0
    def primes():
        yield 2
        it = _odd_iter()  # 初始序列
        while True:
            n = next(it)  # 返回序列的第一个数
            yield n
            it = filter(_not_divisible(n), it)  # 构造新序列
    # 打印100以内的素数:
    for n in primes():
        if n < 100:
            print(n)


# 3、单例模式
import threading
class Singleton(object):
    _instance_lock = threading.Lock()
    def __init__(self):
        pass
    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, '_instance'):
            with Singleton._instance_lock:
                if not hasattr(Singleton, '_instance'):
                    Singleton._instance = object.__new__(cls)
        return Singleton._instance
def test_03():
    def task(arg):
        obj = Singleton()
        print(obj)
    for i in range(10):
        t = threading.Thread(target=task, args=(i,))
        t.start()


# 4、编写汉诺塔模型
# 将a的圆饼移动到c上（借助b）
def test_04():
    def move(n, a, b, c):
        if n == 1:
            print(a, '--->', c)
        else:
            move(n - 1, a, c, b)
            print(a, '--->', c)
            move(n - 1, b, a, c)
    move(4, 'a', 'b', 'c')


test_01()
# test_02()
test_03()
test_04()