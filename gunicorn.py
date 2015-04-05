'''
    gunicorn
    ~~~~~~~~

    Gunicorn 配置
'''

import multiprocessing

bind = '127.0.0.1:9394'
workers = multiprocessing.cpu_count() * 2

forwarded_allow_ips = ','.join([
    '127.0.0.1',
])

raw_env = []
