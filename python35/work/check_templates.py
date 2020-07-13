# coding=utf8
import requests
from lxml import etree
import re

base_url = 'https://wap.sogou.com/web/searchList.jsp?htprequery=%s&keyword=%s&pg=webSearchList'
#base_url = 'https://wap.sogou.com/web/searchList.jsp?&v=5&dp=1&w=1283&t=1594021163211&s_t=1594022107768&s_from=result_up&htprequery=%s&keyword=%s&pg=webSearchList&rcer=RiEntuvq&s=搜索&suguuid=d32aada6-cb60-43a5-8e20-69222b73b030&sugsuv=AAHIHmlPLwAAAAqgDEUobgAAkwA&sugtime=1594022107767'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.04'}
#ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53'
#headers = {'User-Agent': ua}

def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

def is_contains_alpha(s):
    for ch in s:
        if ch.isalpha():
            return True
    return False

line = '圣墟'
url = base_url % (line, line)
r = requests.get(url, headers=headers)
text = r.text

print(text)
tree = etree.HTML(text)
site_l1 = tree.xpath(u"//span[@class]/text()")
re_pat = re.compile(r'<span.*?>(.*?)</span>')
site_l2 = re.findall(re_pat, text)


site_l = site_l1 + site_l2
print(site_l)
site_s = set(site_l)
site_res = [s for s in site_s if not is_contains_chinese(s) and is_contains_alpha(s)]
print(site_res)
