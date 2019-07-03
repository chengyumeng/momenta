#!/usr/bin/env python
# -*- coding: utf-8 -*

import requests
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
        url ='https://www.mxnzp.com/api/holiday/single/{}'.format(datetime.date.today().strftime('%Y%m%d'))
        headers = {'cache-control': 'no-cache'}
        dateInfo = json.loads(requests.request('GET', url, headers=headers).text)
        url = "https://api.hibai.cn/api/index/index"
        payload = 'TransCode=030111&OpenId=123456789'
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        motto = json.loads(response.text)
        return msg.format(dateInfo['data']['date'], dateInfo['data']['weekOfYear'], dateInfo['data']['dayOfYear'],
                          motto['Body']['word'], motto['Body']['word_from'])
    except Exception as e:
        print(e)
        return msg.format(datetime.datetime, 'x','y',e, 'momenta 出现异常！')


