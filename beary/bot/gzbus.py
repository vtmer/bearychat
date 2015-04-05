# coding: utf-8

'''
    beary.bot.gzbus
    ~~~~~~~~~~~~~~~

    妈妈再也不用担心我赶不上广州的公交啦 ～(^з^)-☆

    机器人命令格式：

        > /gzbus 番52路 中环西路站
        > /gzbus 番52路
'''

from __future__ import absolute_import

import re
import gzbus

from .utils import must_reply


__all__ = ['handle']


def _unable_to_handle(text=None):
    text = text or '不能处理哦'
    return {
        'text': text,
        'attachments': []
    }


def _extract_routine_and_current_stop(raw):
    '''提取查询的路线和当前车站

    当提取失败时，ヽ( ｀0´)ﾉ ``ValueError``

    :param raw: 用户查询
    '''
    p = re.compile('^/\S+\s(\S+)\s?(\S+)?$')
    rv = p.findall(raw)
    if not rv:
        raise ValueError('unable to parse: {0}'.format(raw))
    routine, bus_stop = rv[0]

    # 为了满足渣渣的 gzbus 编码 /w\
    if isinstance(routine, unicode):
        routine, bus_stop = routine.encode('u8'), bus_stop.encode('u8')
    if not bus_stop:
        bus_stop = None
    return routine, bus_stop


def _query(routine, bus_stop):
    '''进行查询

    TODO 缓存查询结果 ٩◔̯◔۶

    :param routine: 公交路线名称
    :param bus_stop: 当前等待公交站
    '''
    return gzbus.query_realtime_routine(routine, bus_stop)


def _translate_query_result(query_result):
    '''将 gzbus 的查询结果翻译成人类看得懂的形式

    :param query_result: gzbus 查询结果
    '''
    tmpl = ('往 {destinate_station} 方向：到 {waiting_station} '
            '还有 {distance} 站')
    translate_dir = lambda d: tmpl.format(**d['current'])

    return '\n'.join(map(translate_dir, query_result))


@must_reply(_unable_to_handle)
def handle(payload):
    routine, bus_stop = _extract_routine_and_current_stop(payload['text'])
    query_result = _query(routine, bus_stop)
    result = _translate_query_result(query_result)

    return {'text': result, 'attachments': []}
