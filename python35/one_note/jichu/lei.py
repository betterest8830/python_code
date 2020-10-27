# coding=utf8


# __mro__
class A(object):
    def __init__(self):
        print("enter A")
        super(A, self).__init__()  # 可以注释之后看看
        print("leave A")
class B(object):
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
f = F()
print(F.__mro__)


# 实例变量 和 类变量
class Person(object):
    name = 'aaa'
p1 = Person()
p2 = Person()
p1.name = 'bbb'
print(p1.name, p2.name)
del p1.name
print(p1.name)
print(Person.name)