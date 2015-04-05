# coding: utf-8

'''
    manager
    ~~~~~~~

    大家来管管这个熊孩子 (｀･ω･´)
'''

import click

from beary.app import build


app = build()


@click.group()
def main():
    pass


@main.command()
@click.option('--host', default='127.0.0.1', help='serve host')
@click.option('--port', default=9394, help='serve port')
def run(host, port):
    '''运行一下本地开发程序'''
    app.run(host=host, port=port, debug=True)


if __name__ == '__main__':
    main()
