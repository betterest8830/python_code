# coding=utf8

import collections

height = [2868,5485,1356,1306,6017,8941,7535,4941,6331,6181]
weight = [5042,3995,7985,1651,5991,7036,9391,428,7561,8594]
matrix = sorted(zip(height, weight), key=lambda x:x[0])
#print(matrix)

a='123232'
b='23433'
c, d = collections.Counter(a), collections.Counter(b)
e, f = c&d, c | d
print(c, d)
print(e, f)

print([]+ [12])
print([].append(12))