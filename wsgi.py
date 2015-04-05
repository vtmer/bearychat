# coding: utf-8

'''
    wsgi
    ~~~~

    WSGI 程序 (｀･ω･´).
'''

from werkzeug.contrib.fixers import ProxyFix

from beary.app import build


app = ProxyFix(build())
