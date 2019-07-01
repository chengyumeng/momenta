#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
import pymongo
import schedule
from pkg.bot.wechat import do_send_message
from pkg.cron.cron import app

client = pymongo.MongoClient('mongodb://%s:%s@%s' % (os.getenv('MOMENTA_MONGO_USER'), os.getenv('MOMENTA_MONGO_PASSWORD'),os.getenv('MOMENTA_MONGO_HOST')))


def daily_job():
    for data in client.momenta.subscription.find({'enable': True},
                                                 {'_id': 0, 'trigger': 1, 'nickname': 1, 'action': 1}):
        do_send_message(data['nickname'], app.do(data['action']))


def regist_job():
    try:
        schedule.every().day.at('10:32').do(daily_job)
    except Exception as e:
        print(e)