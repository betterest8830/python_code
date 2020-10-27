# coding=utf8

import threading


# 使用装饰器
def singleton(cls):
    _instance = {}
    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return _singleton
@singleton
class A(object):
    a = 1
    def __init__(self, x=0):
        self.x = x
print(A(2))
print(A(3))

# 使用类
class Singleton(object):
    _instance_lock = threading.Lock()
    def __init__(self):
        pass
    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(Singleton, '_instance'):
            with Singleton._instance_lock:
                if not hasattr(Singleton, '_instance'):
                    Singleton._instance = Singleton(*args, **kwargs)
        return Singleton._instance


# 使用__new__方法
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


# 使用metaclass方式(第一个非单利模式)
class SingletonType(type):
    def __new__(cls, name, bases, attrs):
        print('cls0: ', cls)
        return type.__new__(cls, name, bases, attrs)
    def __init__(cls, *args, **kwargs):
        print('cls1: ', cls)
        print('create class run')
        super().__init__(*args, **kwargs)
    def __call__(cls, *args, **kwargs):
        print('cls2: ', cls)
        obj = cls.__new__(cls, *args, **kwargs)
        cls.__init__(obj, *args, **kwargs)
        return obj
class Foo(metaclass=SingletonType):
    def __init__(self, name):
        self.name = name
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)
f = Foo('f')
class SingletonType2(type):
    _instance_lock = threading.Lock()
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with SingletonType2._instance_lock:
                if not hasattr(cls, '_instance'):
                    cls._instance = super(SingletonType2, cls).__call__(*args, **kwargs)
        return cls._instance
class Foo2(metaclass=SingletonType2):
    def __init__(self, name):
        self.name = name
print(Foo2('f1'), Foo2('f2'))

