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


d1 = {'a': 1, 'b': 0, 'c': -3, 'd': 3}
print(sorted(d1.items(), key=lambda x: abs(x[1]), reverse=True))

d2 = {1:2, 2:3, 4:3, 3:5, 6:5}
d_new = {}
for k, v in d2.items():
    if v not in d_new:
        d_new[v] = []
    d_new[v].append(k)
print(d_new)
res, stk = [], [3]
while stk:
    up = stk.pop()
    lowers = d_new.get(up,[])
    for low in lowers:
        stk.append(low)
        res.append(low)
print(res)







