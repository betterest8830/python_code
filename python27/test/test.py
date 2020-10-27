# coding:utf-8
import threading, time
import sys

print sys.getcheckinterval()


a = [-2, -5, 6, 3]
b = ['1', '5', '21', '4']
print sorted(b, cmp=lambda x, y: -1 if x+y < y+x else 1)

import urlparse
url='http://www.chenxm.cc/post/719.html'
res = urlparse.urlparse(url)
netloc = res.netloc
print netloc



def upper_attr(future_class_name, future_class_parents, futrue_class_attr):
    attrs = ((name, value) for name, value in futrue_class_attr.items() if not name.startswith('__'))
    uppercase_attr = dict((name.upper(), value) for name, value in attrs)
    print uppercase_attr
    return type(future_class_name, future_class_parents, uppercase_attr)


class Foo(object):
    __metaclass__ = upper_attr
    bar = 'bip'
print hasattr(Foo, 'bar')
print hasattr(Foo, 'BAR')


# __mro__
class A:
    def __init__(self):
        print("enter A")
        super(A, self).__init__()
        print("leave A")
class B:
    def __init__(self):
        print("enter B")
        super(B, self).__init__()
        print("leave B")
class C(A):
    def __init__(self):
        print("enter C")
        super(C, self).__init__()
        print("leave C")
class D(A):
    def __init__(self):
        print("enter D")
        super(D, self).__init__()
        print("leave D")
class E(B, C):
    def __init__(self):
        print("enter E")
        super(E, self).__init__()
        print("leave E")
class F(E, D):
    def __init__(self):
        print("enter F")
        super(F, self).__init__()
        print("leave F")
f = A()
# print(F.__mro__)