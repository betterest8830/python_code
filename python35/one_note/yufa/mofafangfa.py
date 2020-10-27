# coding=utf8

# __new__ 方法
class Test(object):
    def __new__(cls, *args, **kwargs):
        print('__new__')
        return object.__new__(cls)
    def __init__(self, test_name):
        print('__init__')
        self.test_name = test_name
print(Test('Json').test_name)