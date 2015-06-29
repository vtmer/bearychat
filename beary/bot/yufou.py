# coding: utf-8

'''
    beary.bot.yufou
    ~~~~~~~~~~~~~~~

    广州待会会下雨吗？

    机器人命令格式：

        > /yufou  待会下雨吗？
'''

from __future__ import absolute_import

import yufou
import requests
from datetime import datetime, timedelta

from .utils import must_reply


__all__ = ['handle']


RADAR_STATION = 'AZ9200'


def _unable_to_handle(text=None):
    text = text or '不能处理哦'
    return {
        'text': text,
        'attachments': []
    }


def _get_image():
    prev_5_minutes = timedelta(minutes=5)
    at = datetime.utcnow()
    image = None
    while True:
        image = yufou.radar.image(RADAR_STATION, at=at)

        # 图片请求失败，尝试获取 5 分钟前的
        if not requests.get(image).ok:
            at = at - prev_5_minutes
            continue

        return image


@must_reply(_unable_to_handle)
def handle(payload):
    image = _get_image()

    return {
        'text': '快看',
        'attachments': [{
            'title': '广州雷达',
            'text': '广州雷达',
            'color': '#fff',
            'images': [
                {'url': image}
            ]
        }]
    }
