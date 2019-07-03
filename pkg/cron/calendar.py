#!/usr/bin/env python
# -*- coding: utf-8 -*

import http.client
import datetime
import json

from pkg.cron.cron import app

msg = """今天是 {},今年的第 {} 周，全年已经过去 {} 天

{}
—— {}
"""


@app.action('calendar')
def calendar():
    try:
        conn = http.client.HTTPSConnection('https://www.mxnzp.com')
        headers = {'cache-control': 'no-cache'}
        conn.request('GET', '/api/holiday/single/{}'.format(datetime.date.today().strftime('%Y%m%d')), headers=headers)
        dateInfo = json.loads(conn.getresponse().read().decode('utf-8'))
        conn = http.client.HTTPSConnection('https://api.hibai.cn')
        payload = 'TransCode=030111&OpenId=123456789'
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
        }
        conn.request('POST', '/api/index/index', payload, headers)
        motto = json.loads(conn.getresponse().read().decode('utf-8'))
        return msg.format(dateInfo['data']['date'], dateInfo['data']['weekOfYear'], dateInfo['data']['dayOfYear'],
                          motto['Body']['word'], motto['Body']['word_from'])
    except Exception as e:
        print(e)
        return msg.format(datetime.datetime, 'x','y',e, 'momenta 出现异常！')


