#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# 1、使用模块
class Singleton(object):
    def foo(self):
        pass
singleton = Singleton()
# from a import singleton


# 2、使用装饰器
def singleton(cls):
    _instance = {}
    def _singleton(*args, **kw):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kw)
        return _instance[cls]
    return _singleton
@singleton
class A(object):
    a = 1
    def __init__(self, x=0):
        self.x = x
def test_2():
    # 用函数装饰类：语法糖等价A = singleton(A)
    print(A(2).x)  # 2
    print(A(3).x)  # 2


# 3、使用类(双重判断加锁支持多线程模式)
import threading
class Singleton(object):
    _instance_lock = threading.Lock()
    def __init__(self):
        pass
    @classmethod
    def instance(cls, *args, **kw):
        if not hasattr(Singleton, '_instance'):
            with Singleton._instance_lock:
                if not hasattr(Singleton, '_instance'):
                    Singleton._instance = Singleton(*args, **kw)
        return Singleton._instance
def test_3():
    # 这种方式实现的单例模式，使用时会有限制，以后实例化必须通过 obj = Singleton.instance()
    # 如果用 obj=Singleton() ,这种方式得到的不是单例
    def task(arg):
        obj = Singleton.instance()
        print(obj)
    for i in range(10):
        t = threading.Thread(target=task, args=(i,))
        t.start()


# 4、使用__new__方法
class Singleton(object):
    _instance_lock = threading.Lock()
    def __init__(self):
        pass
    def __new__(cls, *args, **kw):
        if not hasattr(Singleton, '_instance'):
            with Singleton._instance_lock:
                if not hasattr(Singleton, '_instance'):
                    Singleton._instance = object.__new__(cls)
        return Singleton._instance
def test_4():
    # 和平时实例化对象的方法一样 obj = Singleton()
    def task(arg):
        obj = Singleton()
        print(obj)
    for i in range(10):
        t = threading.Thread(target=task, args=(i,))
        t.start()


# 5、基于metaclass方式实现
"""
1.类由type创建，创建类时，type的__init__方法自动执行，类() 执行type的 __call__方法(类的__new__方法,类的__init__方法)
2.对象由类创建，创建对象时，类的__init__方法自动执行，对象()执行类的 __call__ 方法
"""
class SingletonType0(type):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
    def __call__(cls, *args, **kw):
        print('cls: ', cls)
        obj = cls.__new__(cls, *args, **kw)
        cls.__init__(obj, *args, **kw)
        return obj
class Foo0(metaclass=SingletonType0):
    def __init__(self, name):
        self.name = name

    def __new__(cls, *args, **kw):
        return object.__new__(cls)
class SingletonType(type):
    _instance_lock = threading.Lock()
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with SingletonType._instance_lock:
                if not hasattr(cls, '_instance'):
                    cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance
class Foo(metaclass=SingletonType):
    def __init__(self, name):
        self.name = name
def test_5():
    obj = Foo0('XX')
    obj1 = Foo('name')
    obj2 = Foo('name')
    print(obj1, obj2)


# test_2()
# test_3()
# test_4()
test_5()