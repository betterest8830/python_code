# coding=utf8


import datetime
import time

'''

s = 'Tue Aug 25 18:10:36 2020'
s = time.strptime(s, "%a %b %d %H:%M:%S %Y")
print(s)
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

import hashlib

def curlmd5(src):
    m = hashlib.md5()
    m.update(src.encode('UTF-8'))
    return m.hexdigest()
print(curlmd5('333'))


'''
import sys, os, time, datetime, shutil
import smtplib
from email.mime.text import MIMEText
from email.mime.text import MIMENonMultipart

print(0/float('inf'))
print(0/float('-inf'))
print(0/float('inf') == 0/float('-inf'))

x = {"apple", "banana", "cherry"}
y = [1,2,3]

x.update(y)
print(x)