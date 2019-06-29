#!/usr/bin/env python
# -*- coding: utf-8 -*

import click
import os
import pymongo
from bson.objectid import ObjectId
import schedule
import itchat
import _thread
import time

from pkg.bot.wechat import do_send_message
from pkg.bot.callback import callback
from pkg.cron.cron import app

Daily = 'daily'
Sunday = 'sunday'
Mounday = ''

client = pymongo.MongoClient('mongodb://%s:%s@%s' % (os.getenv('MOMENTA_MONGO_USER'), os.getenv('MOMENTA_MONGO_PASSWORD'),os.getenv('MOMENTA_MONGO_HOST')))


@click.group(help='与群组、好友咨询订阅相关的操作')
def subscription():
    pass


@click.command(help='列出所有的订阅')
def list_subscription():
    for data in client.momenta.subscription.find({}, {'_id': 1, 'trigger': 1, 'nickname': 1,'enable': 1,'action': 1}):
        print(data)


@click.command(help='创建一个订阅')
@click.option('--trigger', default=Daily, help='订阅触发的周期')
@click.option('--nickname', default='', help='订阅用户、群组的名字')
@click.option('--action', default='', help='订阅行为')
@click.option('--enable', default=True, help='是否默认生效')
def create_subscription(trigger, nickname, action, enable):
    id = client.momenta.subscription.insert_one(
        {'trigger': trigger, 'nickname': nickname, 'action': action, 'enable': enable}).inserted_id
    print(id)


@click.command(help='删除一个订阅')
@click.option('--force', default=False, help='是否彻底删除一条订阅')
@click.argument('id')
def remove_subscription(force, id):
    if force:
        x = client.momenta.subscription.delete_one({'_id': ObjectId(id)})
    else:
        x = client.momenta.subscription.update_one({'_id': ObjectId(id)}, {'$set': {'enable': False}})
    print(x)


@click.command(help='标记一个订阅为可用')
@click.option('--id', default='', help='待订阅订阅的 ID')
def enable_subscription(id):
    x = client.momenta.subscription.update_one({'_id': ObjectId(id)}, {"$set": {"enable": True}})
    print(x)


subscription.add_command(list_subscription, name='list')
subscription.add_command(create_subscription, name='create')
subscription.add_command(remove_subscription, name='remove')
subscription.add_command(enable_subscription, name='enable')


@click.command()
def run():
    itchat.auto_login(hotReload=True)
    callback.xiaoice = itchat.search_mps(name='小冰')[0]['UserName']
    for data in client.momenta.subscription.find({'enable': True}, {'_id': 0, 'trigger': 1, 'nickname': 1, 'action': 1}):
        try:
            schedule.every().day.at("10:15").do(do_send_message,data['nickname'], app.do(data['action']))
        except Exception as e:
            print(e)

    def sche():
        while True:
            schedule.run_pending()
            time.sleep(1)
            print('scheduling job {}'.format(time.time()))

    _thread.start_new_thread(sche, ())
    _thread.start_new_thread(callback.consume,())
    itchat.run(True)


@click.group()
def cli():
    pass


@click.command()
def version():
    print('momenta {}'.format('beta'))


cli.add_command(subscription)
cli.add_command(run)
cli.add_command(version)


def main():
    cli()
