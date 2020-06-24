#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''
# UnboundLocalError: local variable 'a_var' referenced before assignment
a_var = 1
def a_func():
    a_var = a_var + 1
    print(a_var, '[ a_var inside a_func() ]')
print(a_var, '[ a_var outside a_func() ]')
a_func()
'''


a = 'global'
def outer():
    def len(in_var):
        print('called my len() function: ', end="")
        l = 0
        for i in in_var:
            l += 1
        return l
    a = 'local'
    def inner():
        global len
        nonlocal a
        a += ' variable'
    inner()
    print('a is', a)
    print(len(a))
outer()
print(len(a))
print('a is', a)
'''
a is local variable
called my len() function: 14
6
a is global
'''


# 这种结果没有问题，但是建议不要这么使用
for a in range(5):
    if a == 4:
        print(a, '-> a in for-loop')
print(a, '-> a in global')
'''
# NameError: name 'b' is not defined
for b in range(0):
    pass
print(b)

NameError: name 'i' is not defined
print([i for i in range(5)])
print(i, '-> i in global')
'''


a = [[1, 2, 3]] * 2
print(id(a[0]), id(a[1]))  # 1634623272712 1634623272712