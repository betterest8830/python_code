#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Xu'

"""
爬虫西刺
"""

import threading
import time
import json
from threading import Lock

import requests
from lxml import etree
from pymongo import MongoClient as Client
import redis
import pymysql

import logging
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)-8s %(message)s',
                    filename='data/xici/test.log', filemode='w')

ua = 'Mozilla/5.0 (Linux; U; Android 4.4.4; ' \
     'Nexus 5 Build/KTU84P) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
headers = {'User-Agent': ua}
g_lock = Lock()


# 将获得的ip转化成代理格式
def dict2proxy(dic):
    s = dic['type'] + '://' + dic['ip'] + ':' + str(dic['port'])

    return {'http': s, 'https': s}


# 获取网页的ip、port、type(HTTP or HTTPS)
def parse_item(items):
    ips = []
    for item in items:
        ip = item.xpath('./td[2]/text()')[0]
        port = item.xpath('./td[3]/text()')[0]
        _type = item.xpath('./td[6]/text()')[0]
        ips.append({'ip': ip, 'port': port, 'type': _type})

    return ips


# 检查获取的ip是否有效
def check(ip):
    try:
        pro = dict2proxy(ip)
        url = 'https://www.ipip.net/'
        r = requests.get(url, headers=headers, proxies=pro, timeout=5)
        r.raise_for_status()  # 如果不是200则产生一个HttpError的异常
    except Exception as e:
        logging.info('check fail! url: %s error: %s' % (url, e))
        return False
    else:
        logging.info('check success!')
        return True


# 抓取某个网页的内容
def get_proxies(index):
    try:
        url = 'https://www.xicidaili.com/nt/%s' % index
        r = requests.get(url, headers=headers, timeout=5)
        tree = etree.HTML(r.content.decode('utf-8'))
        items = tree.xpath('//tr[@class]')
        ips = parse_item(items)
    except Exception as e:
        logging.info('scrapy failure! url: %s, error: %s' % (url, e))
    else:
        logging.info('scrapy success!')
    finally:
        logging.info('scrapy end.')

    ips = ips[:10]
    good_proxies = []
    for ip in ips:
        if check(ip):
            good_proxies.append(ip)
    return good_proxies


# 读取json文件中的数据
def read_json():
    with open('data/xici/proxies.json', 'r', encoding='utf-8') as f:
        return json.load(f)


# 将有效ip存储到json文件中
def write_to_json(ips):
    with open('data/xici/proxies.json', 'w', encoding='utf-8') as f:
        json.dump(ips, f, indent=4)


# 将有效ip存储到mongo数据库中
def write_to_mongo(ips):
    client = Client(host='localhost', port=27017)
    db = client['proxies_db']
    coll = db['xici_proxies']
    for ip in ips:
        if coll.find({'ip': ip['ip']}).count() == 0:
            coll.insert_one(ip)
    client.close()


# 将有效ip存储到redis数据库中
def write_to_redis(ips):
    r = redis.Redis(host='localhost', port=6379, db=4, password=None)
    for ip in ips:
        r.sadd('xici_proxies', str(ip))


# 将有效ip存储到mysql数据库中
def write_to_mysql(ips):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='password', database='study', charset='utf8')
    cursor = conn.cursor()
    # cursor.execute('create table xici_proxies (ip varchar(20) primary key, port INTEGER , type_s varchar(10))')
    for temp in ips:
        ip, port, _type = temp['ip'], temp['port'], temp['type']
        cursor.execute('SELECT ip FROM xici_proxies')
        ip_s = set()
        for tmp in cursor.fetchall():
            ip_s.add(tmp[0])
        if ip in ip_s:
            continue
        cursor.execute('insert into xici_proxies (ip, port, type_s) values (%s, %s, %s)', [ip, port, _type])
        conn.commit()
    cursor.close()
    pass


# 单线程测试
def test():
    good_proxies = get_proxies(1)
    write_to_json(good_proxies)
    # good_proxies = readjson()
    # write_to_mongo(good_proxies)
    # write_to_redis(good_proxies)
    # write_to_mysql(good_proxies)
    pass


# 多线程检查ip并保存不需要锁
def check_ip(ip, good_proxies):
    try:
        pro = dict2proxy(ip)
        url = 'http://www.ipip.net/'
        r = requests.get(url, headers=headers, proxies=pro, timeout=5, verify=False)
        r.raise_for_status()  # 如果不是200则产生一个HttpError的异常
    except Exception as e:
        logging.info('check fail! proxy: %s error: %s' % (pro, e))
    else:
        logging.info('check success!')
        good_proxies.append(ip)


def check_ip_lock(ip):
    try:
        pro = dict2proxy(ip)
        url = 'https://www.ipip.net/'
        r = requests.get(url, headers=headers, proxies=pro, timeout=5)
        r.raise_for_status()  # 如果不是200则产生一个HttpError的异常
    except Exception as e:
        logging.info('check fail! proxy: %s error: %s' % (pro, e))
    else:
        logging.info('check success!')
        g_lock.acquire()
        write_to_json_lock(ip)
        g_lock.release()


# 多线程写文件需要锁住
def write_to_json_lock(ip):
    with open('data/xici/proxies_lock.json', 'a+', encoding='utf-8') as f:
        f.write(str(ip) + '\n')


class GetThread(threading.Thread):
    def __init__(self, args):
        threading.Thread.__init__(self, args=args)
        self.good_proxies = []

    def run(self):
        url = 'https://www.xicidaili.com/nt/%s' % (self._args[0])
        r = requests.get(url, headers=headers, timeout=5, verify=False)
        tree = etree.HTML(r.content.decode('utf-8'))
        items = tree.xpath('//tr[@class]')
        ips = parse_item(items)
        threads = []
        # 验证ip时使用库中线程，也使用多线程。
        for ip in ips:
            # 不用锁
            t = threading.Thread(target=check_ip, args=(ip, self.good_proxies))
            # 需要用锁
            # t = threading.Thread(target=check_ip_lock, args=(ip,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

    def get_results(self):
        return self.good_proxies


def get_all_proxies():
    res_l = []
    threads = []
    for i in range(1, 4):
        t = GetThread(args=(i,))
        t.start()
        time.sleep(2)
        threads.append(t)
    for t in threads:
        t.join()
    for t in threads:
        proxies = t.get_results()
        res_l += proxies

    write_to_json(res_l)
    return res_l


if __name__ == '__main__':
    # test()
    get_all_proxies()
