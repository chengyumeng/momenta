#!/usr/bin/env python
# -*- coding: utf-8 -*

import itchat


class Callback():

    _instance = None
    actions = None
    queue = None
    msg = None
    xiaoice = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls.actions = {}
            cls.queue = []
            cls._instance = super(Callback, cls).__new__(cls, *args, **kw)
        return cls._instance

    def action(self, action_str):
        def decorator(func):
            self.actions[action_str] = func
            return func
        return decorator

    def do(self, path,*args, **kw):
        view_function = self.actions.get(path)
        if view_function:
            return view_function(*args, **kw)
        else:
            raise ValueError('callback "{}" has not been registered'.format(path))

    def add(self, msg):
        self.queue.append(msg)

    def consume(self):
        while True:
            if self.msg is not None:
                continue
            elif len(self.queue) > 0:
                try:
                    self.msg = self.queue.pop(0)
                    itchat.send_msg(self.msg.text, self.xiaoice)
                except Exception as e:
                    print(e)


callback = Callback()


@callback.action('@')
def at(msg):
    msg.text = msg.text[7:]
    callback.add(msg)


@callback.action('/chat')
def do_chat(msg):
    callback.add(msg)


@callback.action('/group/manage')
def do_group_manage(msg):
    print(msg)


