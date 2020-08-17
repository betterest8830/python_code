import requests
from lxml import etree

proxies = {"https": "http://proxy_baidu_jj:baidu_jj@gateway.proxy-center.sogou:9100", "http": "http://proxy_baidu_jj:baidu_jj@gateway.proxy-center.sogou:9100",}

base_url = 'http://m.baidu.com/s?word=%s'
ua = 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.04'

#ua = 'Mozilla/5.0 (Linux; U; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
headers = {'User-Agent': ua}
line = '漫漫追妻路 图图的早晨'
url = 'https://www.uukanshu.com/b/75780/140859.html'
print(url)

r = requests.get(url, headers=headers)
text = r.text
print(text)
#tree = etree.HTML(r.text)
#xpath_title = u"//div[@class='relative color32 pt-read mt20']/div[2]/div/div[1]/a/@href"
#title = tree.xpath(xpath_title)
#print(title)


