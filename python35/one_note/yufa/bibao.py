# coding=utf8


# 闭包后期绑定
def create_multipliers():
    return [lambda x: i*x for i in range(3)]
for m in create_multipliers():
    print(m(2))
def create_multipliers():
    return [lambda x, j=i: j*x for i in range(3)]
for m in create_multipliers():
    print(m(2))
# 优雅的写法是用生成器
for m in (lambda x: i * x for i in range(3)):
    print(m(2))
def create_multipliers():
    for i in range(3):
        yield lambda x: i*x
for m in create_multipliers():
    print(m(2))
