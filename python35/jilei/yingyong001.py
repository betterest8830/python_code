#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''
# 1、字符串是否含有中文

'''


# 1、字符串是否含有中文
def test01():
    # 检验是否全是中文字符
    def is_all_chinese(strs):
        for _char in strs:
            if not '\u4e00' <= _char <= '\u9fa5':
                return False
        return True

    # 检验是否含有中文字符
    def is_contains_chinese(strs):
        for _char in strs:
            if '\u4e00' <= _char <= '\u9fa5':
                return True
        return False
    s = 'abc你好'
    print(is_contains_chinese(s))
    print(is_all_chinese(s))


test01()

