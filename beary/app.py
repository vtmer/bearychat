# coding: utf-8

'''
    beary.app
    ~~~~~~~~~

    很厉害的服务器端程序实例 (｀･ω･´)
'''

from __future__ import absolute_import

from flask import Flask


def init_logging(app):
    '''初始化日志记录设置'''
    # TODO


def init_bot(app):
    '''初始化 bearychat 机器人 I'M A ROBOT'''
    from . import bot

    bot.init(app)


def build(**settings):
    '''构造服务器实例的工厂函数

    （从低到高的）配置加载优先度：

        - 默认的配置： `beary.config.default`
        - 环境变量 `BEARY_SERVER_CONFIG` 指定的配置文件位置
        - 传入工厂函数中的配置

    :param settings: 用作重写的配置对（大写, please!）
    '''
    app = Flask(__name__)

    # 初始化乱七八糟的配置 ☆⌒(*＾-゜)v
    app.config.from_object('beary.config.default')
    app.config.from_envvar('BEART_SERVER_CONFIG', silent=True)
    app.config.update(settings)

    # 带上其他组件一起初始化！(~,~)(~,~)
    init_logging(app)
    init_bot(app)

    return app
