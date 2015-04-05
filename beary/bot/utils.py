# coding: utf-8

'''
    beary.bot.utils
    ~~~~~~~~~~~~~~~

    Gollum: "Pleasure!" (^0_0^)
'''

import logging

from functools import wraps


class must_reply(object):

    def __init__(self, reply_on_error, watched_errors=None):
        self.reply_on_error = reply_on_error
        self.watched_errors = watched_errors or Exception

    def __call__(self, func):
        @wraps(func)
        def trap(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except self.watched_errors as e:
                logging.error(e)
                return self.reply_on_error()
        return trap
