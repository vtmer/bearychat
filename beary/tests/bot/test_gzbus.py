# coding: utf-8

'''
    beary.tests.bot.test_gzbus
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    gzbus 机器人测试用例 ( ´▽｀)
'''

import pytest

from beary.bot.gzbus import _extract_routine_and_current_stop


def test_extract_routine_and_current_stop():
    cases = [
        (u'/gzbus 番52路 中环西路站', ('番52路', '中环西路站')),
        (u'/gzbus 番52路', ('番52路', None))
    ]

    for raw, (expected_routine, expected_bus_stop) in cases:
        routine, bus_stop = _extract_routine_and_current_stop(raw)
        assert expected_routine == routine
        assert expected_bus_stop == bus_stop

    with pytest.raises(ValueError):
        _extract_routine_and_current_stop('something_you_cant_parse')
        routine, bus_stop = _extract_routine_and_current_stop(raw)
