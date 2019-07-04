#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import itchat
from pkg.bot.callback import callback


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
        if msg['Type'] == 'Picture':
            msg['Text'](msg['FileName'])
            itchat.send_image(msg['FileName'], callback.msg.FromUserName)
        elif msg['Type'] == 'Text':
            itchat.send_msg(msg.text, callback.msg.FromUserName)
        elif msg['Type'] == 'VIDEO':
            print(msg)
            msg['Text'](msg['FileName'])
            itchat.send_video( msg['FileName'], callback.msg.FromUserName)
        else:
            print(msg)
            msg['Text'](msg['FileName'])
            itchat.send_video(msg['FileName'], callback.msg.FromUserName)
        callback.msg = None


def do_send_message(nickName, msg):
    data = itchat.search_chatrooms(name=nickName)
    if data is not None:
        for u in data:
            u.send(msg)
    data = itchat.search_friends(name=nickName)
    if data is not None:
        for u in data:
            u.send(msg)