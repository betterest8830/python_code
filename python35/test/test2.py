# coding=utf8


d = {2:'a', 1:'b', 3:'c'}
print(d)
print(list(map(hash, [1,2,3])))
print(list(map(hash, [1.0,2.0,3])))
print(list(map(hash, ['a', 'c', 'b'])))
print(list(map(id, [1,3,2])))
print(list(map(id, [1.0,3.0,2])))
print(list(map(id, ['a', 'c', 'b'])))


import hashlib

s='abc'
md=hashlib.md5()
md.update('abc'.encode('utf8'))
print(md.hexdigest())

sha=hashlib.sha1()
sha.update('abc'.encode('utf8'))
print(sha.hexdigest())