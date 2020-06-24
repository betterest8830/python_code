#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from threading import Thread
import time


def my_counter():
    i = 0
    for _ in range(10**8):
        i = i + 1
    return True


def single_test():
    start_time = time.time()
    for tid in range(4):
        t = Thread(target=my_counter)
        t.start()
        t.join()
    end_time = time.time()
    print('single_time:{}'.format(end_time-start_time))


def multi_test():
    thread_array = {}
    start_time = time.time()
    for tid in range(4):
        t = Thread(target=my_counter)
        t.start()
        thread_array[tid] = t
    for i in range(2):
        thread_array[i].join()
    end_time = time.time()
    print('multi_time:{}'.format(end_time - start_time))


multi_test()
single_test()
