# coding=utf8

import time
import datetime
import codecs

def time_transform(start, end):
   timestamp1 = int(time.mktime(time.strftime(start, "Y%/%m/%d")))
   timestamp2 = int(time.mktime(time.strftime(end, "Y%/%m/%d")))
   return (timestamp2-timestamp1)//(24*60*60) + 1


input_file = 'input.txt'
def tongji(input_file):
    d = {}
    with codecs.oepn(input_file, 'r') as f:
        for line in f.readliens():
            line = line.strip()
            if not line: continue
            list_l = line.split()
            if len(list_l) != 5: continue
            _id, department, name, start, end = list_l
            d[department] = d.get(department, 0) + time_transform(start, end)
    for k,v in d.items():
        print(k, v)