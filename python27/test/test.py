# coding:utf-8
import threading, time
import sys

print sys.getcheckinterval()


a = [-2, -5, 6, 3]
b = ['1', '5', '21', '4']
print sorted(b, cmp=lambda x, y: -1 if x+y < y+x else 1)

import urlparse
url='http://www.chenxm.cc/post/719.html'
res = urlparse.urlparse(url)
netloc = res.netloc
print netloc
