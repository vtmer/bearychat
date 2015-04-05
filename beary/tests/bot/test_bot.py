# coding: utf-8

'''
    beary.tests.bot.test_bot
    ~~~~~~~~~~~~~~~~~~~~~~~~

    机器人模块的测试用例 ( ´▽｀)
'''

import pytest

from beary import bot
from beary.bot.utils import must_reply


def test_get_trigger_word():
    cases = [
        ('/whatever', 'whatever'),
        ('/no_kidding_we_may_use_underscore',
         'no_kidding_we_may_use_underscore'),
        ('/ofCourseCamelCaseIsOk', 'ofCourseCamelCaseIsOk'),
        ('not_starts_with_slash_should_ok', 'not_starts_with_slash_should_ok'),
        ('space is forbidden', None)
    ]

    for original, expected in cases:
        assert expected == bot._get_trigger_word(original)


def test_dispatch_bot():
    echo_bot = lambda x: x
    test_bots = [
        ('test', echo_bot),
    ]
    expected_rv = payload = {'trigger_word': 'test'}
    assert expected_rv == bot._dispatch_bot(payload, test_bots), \
        '普通分发模式'

    default_rv = {'word': 'you know, this is a default response'}
    default_bot = lambda x: default_rv
    test_bots.append((bot._whatever, default_bot))
    assert default_rv == bot._dispatch_bot({}, test_bots), \
        '应该调用默认的机器人配置'

    # 当机器人列表配置不正常时应该抛出异常
    with pytest.raises(ValueError):
        bot._dispatch_bot({}, [])


def test_default_handler():
    assert isinstance(bot._default_handler({}), dict)


def test_must_reply():

    expected_rv = {'some': 'thing'}
    on_fail = lambda *args, **kwargs: expected_rv

    @must_reply(on_fail)
    def catch_all():
        raise Exception
    assert expected_rv == catch_all(), '应该返回擦屁股函数运行结果'

    @must_reply(on_fail, ValueError)
    def catch_value_error():
        raise ValueError
    assert expected_rv == catch_value_error(), '应该返回擦屁股函数运行结果'

    @must_reply(on_fail, ValueError)
    def raises_something_else():
        raise RuntimeError

    with pytest.raises(RuntimeError):
        raises_something_else()
