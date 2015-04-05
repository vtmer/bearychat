# coding: utf-8

'''
    beary.bot
    ~~~~~~~~~

    机器人 I'M A ROBOT (°д°)
'''

from __future__ import absolute_import

import re
from flask import request, jsonify

from . import gzbus


__all__ = ['init', 'BOTS']


def _get_trigger_word(trigger_word_dirty):
    '''获取真正的 trigger word

    如果匹配失败，返回 `None`.

    :param trigger_word_dirty: 请求中的 trigger word.
    '''
    pattern = re.compile('^/?([\w_]+)$')
    matched = pattern.findall(trigger_word_dirty)
    if matched:
        return matched[0]


def _get_bot_endpoint(app):
    '''获取机器人服务器端调用接口'''
    return app.config['BOT_ENDPOINT']


def _dispatch_bot(payload, bots):
    '''根据触发词来分发请求

    :param payload: 请求内容
    :param bots: 分发使用的机器人列表
    '''
    # 默认使用 ``default`` 关键字
    trigger_word = _get_trigger_word(payload.get('trigger_word', '/default'))

    for bot_trigger_word, bot_handler in bots:
        if callable(bot_trigger_word):
            cmp_result = bool(bot_trigger_word(trigger_word))
        else:
            cmp_result = bot_trigger_word == trigger_word

        if cmp_result:
            # 去吧比卡超！ (^-^)V
            return bot_handler(payload)

    # 勇士你不应该走到这里！
    raise ValueError('Invalid trigger payload: {0}'.format(payload))


# 您说是就是了 ㄟ( ▔, ▔ )ㄏ
_whatever = lambda *args, **kwargs: True


def _default_handler(payload):
    '''默认的机器人响应函数

    :param payload: 每个机器人响应函数都应该接收的来自人类的请求参数
    :return: 每个机器人响应函数都应该返回一个 ``dict`` 实例来告诉人类
    '''
    return {
        'text': '(◎_◎;) 不知道你说什么',
        'attachments': []
    }


def init(app):
    '''初始化模块'''

    @app.route(_get_bot_endpoint(app), methods=['POST'])
    def dispatch_bots():
        payload = request.get_json()
        return jsonify(**_dispatch_bot(payload, BOTS))


# 启用了的机器人模块
#
# Night gathers, and now my watch begins.
BOTS = [

    ('gzbus', gzbus.handle),

    # 默认的机器人响应
    (_whatever, _default_handler),
]
