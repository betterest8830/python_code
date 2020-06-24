#!/usr/bin/env python3
# -*- coding: utf-8 -*-


s = {1, 3, 4}
print(type(s))

print(globals())
print(dir(globals()['__builtins__']))

print(bin(5))

print(any('00'))  # True
print(any([0, 0]))  # False

t = (1, 2, 3)
print(t)
print(*t)


foo = [-5, 8, 0, 4, -2]
a = sorted(foo, key=lambda x: (x < 0, abs(x)))
print(type(a), a)


def my_func(total):
    for i in range(total):
        r = yield i
        print(r)


a = my_func(3)
print(a.send(None))
print(a.send('abc'))


import requests
url = 'https://m.suixkan.com/ca/30540.html'
r = requests.get(url)
print(r.text)