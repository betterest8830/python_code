# coding=utf8

import time
from functools import wraps


# 参数装饰器
def use_logging(level):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if level == 'warn':
                print('warn...')
            else:
                print('normal...')
            time.sleep(0.3)
            print('func_name: %s' % func.__name__)  # @wraps(func) 对该函数名会有影响
            return func(*args, **kwargs)
        return wrapper
    return decorator
@use_logging(level='warn')
def foo(a, b):
    print('%s + %s = %s' % (a, b, a+b))
foo(1, 1)
print(foo.__name__)  # @wraps(func) 对该函数名会有影响


# 实现装饰器有参数和无参数功能（方法一）
def log1(text=None):
    print(text)  # 方便理解
    def decorator(func):
        def wrapper(*args, **kwargs):
            if isinstance(text, (int, str)):
                print('%s call func' % text)
                func(*args, **kwargs)
            else:
                print('notext call func')
                func(*args, **kwargs)
        return wrapper
    # 仔细理解
    return decorator if isinstance(text, (int, str)) else decorator(text)
#@log1
@log1(text='yes')
def foo(a, b):
    print('%s + %s = %s' % (a, b, a+b))
foo(1, 2)
# 实现装饰器有参数和无参数功能（方法二）
def log2(*text):
    print(text, *text)
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        return wrapper
    return decorator
@log2()
#@log2('yes')
def foo(a, b):
    print('%s + %s = %s' % (a, b, a+b))
foo(1, 3)


# 类装饰器(类装饰函数)
class Foo(object):
    def __init__(self, func):
        self.func = func
    def __call__(self, *args, **kwargs):
        print('start...')
        self.func(*args, **kwargs)
        print('end...')
@Foo
def foo(a, b):
    print('%s + %s = %s' % (a, b, a+b))
foo(1, 4)
# 函数装饰类
def wrap_class(cls):
    def inner(a):
        print('class name: ', cls.__name__)
        return cls(a)
    return inner
@wrap_class
class Foo():
    def __init__(self, a):
        self.a = a
    def fun(self):
        print('self.a = %s' % self.a)
Foo('lina').fun()