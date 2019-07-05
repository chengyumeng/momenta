#!/usr/bin/env python
# -*- coding: utf-8 -*

import re

from logbook import Logger

from pkg.bot.callback import callback
from pkg.job.client import client
from pkg.bot.wechat import do_send_message

logger = Logger('action')


@callback.action('/chat')
def do_chat(msg):
    callback.add(msg)


@callback.action('/group/manage')
def do_group_manage(msg):
    for data in client.momenta.message.find({'enable': True,'nickname': msg.User.NickName},
                                                 {'_id': 0, 'key': 1, 'regular': 1,'warning':1, 'nickname': 1}):
        try:
            if re.match(data['regular'], msg[data['key']], re.M | re.I) is None:
                do_send_message(data['nickname'], data['warning'])
        except Exception as e:
            logger.error('Failed to do group message'.format(e))