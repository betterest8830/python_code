# coding=utf8
import json
import requests
import logging as L

L.basicConfig(level=L.INFO, format='[%(asctime)s] %(levelname)-8s %(message)s')

g_api_url= 'http://10.134.111.194:8089/crop/op/sensitive/update'
g_platform = 'online'

def open_api_db(thread_i, ckeys_l):
    ckeys_json = json.dumps(ckeys_l)
    data = {
        'userid': 'auto_open',
        'operationsensitive': 'true',
        'ckeys': ckeys_json,
        'platform': g_platform,
    }
    try:
        r = requests.post(g_api_url, data=data)
    except Exception as e:
        L.info('thread_%s POST_FAIL: %s' % (thread_i, e))
        return
    else:
        L.info('thread_%s POST_SUCC: %s' % (thread_i, r.text.encode('gb18030')))


if __name__ == '__main__':
    ckeys_l = ['D5E2EE1E736A80D4E27A637496563339', 'C96E78BEF694DA6296A7CE328C5EEEFB']
    open_api_db(1, ckeys_l)