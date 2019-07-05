#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import itchat

from logbook import Logger

from pkg.bot.callback import callback

logger = Logger('wechat')

@itchat.msg_register(itchat.content.TEXT, True, False)
def text_reply(msg):
    callback.do('/chat',msg)


@itchat.msg_register(itchat.content.TEXT, False, True,)
def text_reply(msg):
    callback.do('/group/manage', msg)
    if msg.IsAt:
        callback.do('@', msg)


@itchat.msg_register([itchat.content.TEXT, itchat.content.PICTURE, itchat.content.FRIENDS, itchat.content.CARD, itchat.content.MAP, itchat.content.SHARING, itchat.content.RECORDING, itchat.content.ATTACHMENT, itchat.content.VIDEO], isMpChat=True)
def map_reply(msg):
    if msg['FromUserName'] == callback.xiaoice:
        try:
            if msg['Type'] == 'Picture':
                msg['Text'](msg['FileName'])
                itchat.send_image(msg['FileName'], callback.msg.FromUserName)
            elif msg['Type'] == 'Text':
                itchat.send_msg(msg.text, callback.msg.FromUserName)
            elif msg['Type'] == 'VIDEO':
                logger.warning(msg)
                msg['Text'](msg['FileName'])
                itchat.send_video( msg['FileName'], callback.msg.FromUserName)
            else:
                logger.warning(msg)
                msg['Text'](msg['FileName'])
                itchat.send_video(msg['FileName'], callback.msg.FromUserName)
            callback.msg = None
        except Exception as e:
            logger.error('Failed to reply map info {}'.format(e))


def do_send_message(nickName, msg):
    try:
        data = itchat.search_chatrooms(name=nickName)
        if data is not None:
            for u in data:
                u.send(msg)
        data = itchat.search_friends(name=nickName)
        if data is not None:
            for u in data:
                u.send(msg)
    except Exception as e:
        logger.error('Failed to send message {}'.format(e))