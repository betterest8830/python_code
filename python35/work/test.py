# coding=utf8

import requests

url = 'http://druidv6.if.qidian.com/argus/api/v1/topBooks/get?site=11&topId=65&categoryId=-1&pageIndex=1&pageSize=20'

ua = 'Mozilla/mobile QDReaderAndroid/7.9.46/490/1000209/6c50662235417218'
headers = {'User-Agent': ua}

cookies = {
    'ywkey': '',
    'ywguid': '',
    'appId': '12',
    'areaId': '30',
    'lang': 'cn',
    'mode': 'normal',
    'bar': '85',
    'qimei': '6c50662235417218',
    'QDInfo': 'CwsTRx0n9YOhlOwpWyibFZz/p7o86X2Pla8swjDQNTPCxbAQG4Yg3Hjkyyg9RdXIEJ00acGq/CmkvILflDkWjYbjU8H6oBHPFTR3sC3Pue8k1ABoe7NRGFCZQAPBWKxK3907/2MRMLwRZQ0RhZqwl6qmADta11XZOcNJ8+YYrp0='
}



s = requests.session()
r = s.get(url, headers=headers, cookies=cookies, verify=False)
print(r.text)