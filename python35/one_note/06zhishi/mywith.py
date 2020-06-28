#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Sample(object):
    def __enter__(self):
        print('in__enter__')
        return 'Foo'
    def __exit__(self, exc_type, exc_val, exc_tb):
        print('in_exit__')
def get_sample():
    return Sample()
with get_sample() as sample:
    print('Sample: ', sample)
'''
in__enter__
Sample:  Foo
in_exit__
'''


class Sample(object):
    def __enter__(self):
        print('in enter')
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print('type:', exc_type)
        print('val:', exc_val)
        print('tb:', exc_tb)
    def do_something(self):
        bar = 1 / 0
        return bar + 10
with Sample() as sample:
    sample.do_something()


# 有多项
with open('1.txt') as f1, open('2.txt') as  f2:
    pass