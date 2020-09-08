#!/usr/bin/env python3
# -*- coding: utf-8 -*-


s = {1, 3, 4}
print(type(s))


print(globals())
print(dir(globals()['__builtins__']))


print(bin(5))


print(any('00'))  # True
print(any(' '))  # True
print(any(''))  # False
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


d = {2:'a', 1:'b', 3:'c'}
print(d)
print(list(map(hash, [1,2,3])))
print(list(map(hash, [1.0,2.0,3])))
print(list(map(hash, ['a', 'c', 'b'])))
print(list(map(id, [1,3,2])))
print(list(map(id, [1.0,3.0,2])))
print(list(map(id, ['a', 'c', 'b'])))


d1 = {'a': 1, 'b': 0, 'c': -3, 'd': 3}
print(sorted(d1.items(), key=lambda x: abs(x[1]), reverse=True))









