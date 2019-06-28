#!/usr/bin/env python
# -*- coding: utf-8 -*


class CronTask():
    _instance = None
    actions = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls.actions = {}
            cls._instance = super(CronTask, cls).__new__(cls, *args, **kw)
        return cls._instance

    def action(self, action_str):
        def decorator(func):
            self.actions[action_str] = func
            return func
        return decorator

    def do(self, path):
        view_function = self.actions.get(path)
        if view_function:
            return view_function()
        else:
            raise ValueError('action "{}" has not been registered'.format(path))


app = CronTask()
