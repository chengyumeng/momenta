#!/usr/bin/env python
# -*- coding: utf-8 -*

import click
from bson.objectid import ObjectId
import schedule
import itchat
import _thread
import time
import sys
import os


from logbook import Logger, StreamHandler
from momenta.bot.wechat import do_send_message

from momenta.job.client import client, regist_job, get_message, set_done
from momenta.bot.callback import callback

Daily = 'daily'
Sunday = 'sunday'
Mounday = ''

StreamHandler(sys.stdout).push_application()

logger = Logger('cli')


@click.group(help='与群组、好友咨询订阅相关的操作')
def subscription():
    pass


@click.command(help='列出所有的订阅')
def list_subscription():
    for data in client.momenta.subscription.find({}, {'_id': 1, 'trigger': 1, 'nickname': 1,'enable': 1,'action': 1}):
        logger.info(data)


@click.command(help='创建一个订阅')
@click.option('--trigger', default=Daily, help='订阅触发的周期')
@click.option('--nickname', default='', help='订阅用户、群组的名字')
@click.option('--action', default='', help='订阅行为')
@click.option('--enable', default=True, help='是否默认生效')
def create_subscription(trigger, nickname, action, enable):
    id = client.momenta.subscription.insert_one(
        {'trigger': trigger, 'nickname': nickname, 'action': action, 'enable': enable}).inserted_id
    logger.info(id)


@click.command(help='删除一个订阅')
@click.option('--force', default=False, help='是否彻底删除一条订阅')
@click.argument('id')
def remove_subscription(force, id):
    if force:
        x = client.momenta.subscription.delete_one({'_id': ObjectId(id)})
    else:
        x = client.momenta.subscription.update_one({'_id': ObjectId(id)}, {'$set': {'enable': False}})
    logger.warning('Success to remove subscription {}'.format(x))


@click.command(help='标记一个订阅为可用')
@click.option('--id', default='', help='待订阅订阅的 ID')
def enable_subscription(id):
    x = client.momenta.subscription.update_one({'_id': ObjectId(id)}, {"$set": {"enable": True}})
    logger.info('Success to enable subscription {}'.format(x))


subscription.add_command(list_subscription, name='list')
subscription.add_command(create_subscription, name='create')
subscription.add_command(remove_subscription, name='remove')
subscription.add_command(enable_subscription, name='enable')


@click.group(help='制定消息过滤规则')
def filter():
    pass

@click.command(help='创建一个消息过滤规则')
@click.option('--key', default='ActualNickName', help='订阅触发的周期')
@click.option('--nickname', default='', help='匹配数据 nickname(群名、好友名字)')
@click.option('--regular', default='', help='匹配正则')
@click.option('--warning', default='', help='警告信息')
@click.option('--enable', default=True, help='是否默认生效')
def create_filter(key, nickname, regular, warning, enable):
    id = client.momenta.message.insert_one(
        {'key': key, 'nickname': nickname, 'regular': regular, 'warning': warning,'enable': enable}).inserted_id
    logger.info(id)


filter.add_command(create_filter, name='create')


def sche():
    while True:
        schedule.run_pending()
        time.sleep(15)
        logger.info('scheduling job {}'.format(time.time()))
        logger.info(schedule.jobs)


@click.command(help='启动一个微信机器人')
@click.option('--cmdqr', default=False, help='是否通过控制台输出二维码')
def run(cmdqr):
    if cmdqr:
        itchat.auto_login(hotReload=True, enableCmdQR=2)
    else:
        itchat.auto_login(hotReload=True)
    callback.xiaoice = itchat.search_mps(name='中关村男子图鉴')[0]['UserName']

    _thread.start_new_thread(callback.consume, ())
    regist_job()
    _thread.start_new_thread(sche, ())

    itchat.run(True)

@click.command(help='启动定时推送的微信机器人')
@click.option('--cmdqr', default=False, help='是否通过控制台输出二维码')
def run2(cmdqr):
    if cmdqr:
        itchat.auto_login(hotReload=True, enableCmdQR=2)
    else:
        itchat.auto_login(hotReload=True)
    def job():
        try:
            msg = get_message()
            print('{}   {}'.format(os.getenv("MOMENTA_SEND_TO"), msg[0][1]))
            do_send_message(os.getenv("MOMENTA_SEND_TO"), msg[0][1])
            set_done(str(msg[0][0]))
        except Exception as e:
            print(e)
    schedule.every().day.at("13:20").do(job)
    schedule.every().day.at("10:15").do(job)
    schedule.every().day.at("20:50").do(job)

    _thread.start_new_thread(sche, ())

    itchat.run(True)


@click.group()
def cli():
    pass


@click.command()
def version():
    logger.info('momenta {}'.format('beta'))


cli.add_command(subscription)
cli.add_command(run)
cli.add_command(run2)
cli.add_command(version)
cli.add_command(filter)



def main():
    cli()
