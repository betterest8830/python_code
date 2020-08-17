# coding=utf8


a = []
a = [a, a, None]
print(a)  # [[], [], None]
a = []
a[:] = [a, a, None]
print(a)  # [[...], [...], None]