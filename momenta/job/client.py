#!/usr/bin/env python
# -*- coding: utf-8 -*

import os

import pymongo
import MySQLdb
import schedule
from logbook import Logger

from momenta.bot.wechat import do_send_message
from momenta.cron.cron import app

logger = Logger('client')

client = pymongo.MongoClient('mongodb://%s:%s@%s' % (os.getenv('MOMENTA_MONGO_USER'), os.getenv('MOMENTA_MONGO_PASSWORD'),os.getenv('MOMENTA_MONGO_HOST')))

mydb = MySQLdb.connect(charset='utf8mb4', passwd=os.getenv('MOMENTA_MYSQL_PASSWD'), port=int(os.getenv('MOMENTA_MYSQL_PORT')),db="momenta",host=os.getenv('MOMENTA_MYSQL_HOST'),user=os.getenv('MOMENTA_MYSQL_USER'))

def daily_job():
    for data in client.momenta.subscription.find({'enable': True},
                                                 {'_id': 0, 'trigger': 1, 'nickname': 1, 'action': 1}):
        msg = app.do(data['action'])
        print('{}   {} \n {}'.format(data['nickname'], data['action'], msg))
        do_send_message(data['nickname'], msg)


def get_message():
    mycursor = mydb.cursor()
    mycursor.execute("select * from message where done = 0 limit 5")
    myresult = mycursor.fetchall()
    return myresult

def set_done(mid):
    print("set done")
    mycursor = mydb.cursor()
    data = mycursor.execute("update message set done=1 where id=" + mid)
    print(data)
    mydb.commit()



def regist_job():
    try:
        schedule.every().day.at('10:32').do(daily_job)
    except Exception as e:
        logger.error('Failed to regist job: '.format(e))