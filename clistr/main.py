# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import sys
import traceback

import click
from click_anno import click_app

from .utils import parse_as_slice


class BaseApp:
    def _read_core(self):
        raise NotImplementedError

    def _is_read(self):
        return not sys.stdin.isatty()

    def _read(self):
        return [] if sys.stdin.isatty() else self._read_core()


class CommonApp(BaseApp):

    def len(self):
        '''show len of str'''
        for line in self._read():
            click.echo(len(line))

    def skip(self, length: int, from_right=False):
        '''skip number of char from stdin.'''
        for line in self._read():
            if len(line) <= length:
                click.echo('')
            else:
                click.echo(line[length:])

    def rskip(self, length: int):
        '''skip number of char from stdin (from right).'''
        for line in self._read():
            if len(line) <= length:
                click.echo('')
            else:
                click.echo(line[:len(line) - length])

    def take(self, length: int):
        '''take number of char from stdin.'''
        for line in self._read():
            if len(line) <= length:
                click.echo(line)
            else:
                click.echo(line[:length])

    def rtake(self, length: int):
        '''take number of char from stdin (from right).'''
        for line in self._read():
            if len(line) <= length:
                click.echo(line)
            else:
                click.echo(line[len(line) - length:])

    def range(self, start: int, end: int=None):
        '''same as python str[START:END]'''
        for line in self._read():
            val = line[start:end]
            click.echo(val)

    def slice(self, ctx: click.Context, range_str: str):
        slice = parse_as_slice(range_str)
        if not slice:
            ctx.fail(f'{range_str} is not a range')
        for line in self._read():
            click.echo(line[slice])

    def char(self, index: int):
        '''get char by index from stdin.'''
        for line in self._read():
            try:
                val = line[index]
            except IndexError:
                val = ''
            click.echo(val)

    def index_of(self, value: str):
        '''find index of value from stdin.'''
        for line in self._read():
            click.echo(line.find(value))

    def replace(self, old, new):
        '''replace from OLD to NEW.'''
        for line in self._read():
            click.echo(line.replace(old, new))

    def insert(self, value, index: int=0):
        '''insert into source.'''
        for line in self._read():
            if len(line) <= index:
                line = line.ljust(index)
            line = line[:index] + value + line[index:]
            click.echo(line)

    def upper(self):
        '''to upper case.'''
        for line in self._read():
            click.echo(line.upper())

    def lower(self):
        '''to lower case.'''
        for line in self._read():
            click.echo(line.lower())

    def split(self, spliter: str, end: str=None):
        '''split value by spliter.'''
        for line in self._read():
            for x in line.split(spliter):
                click.echo(x)
            if end != None:
                click.echo(end)

    _cc_modes = [
        'hk2s', 's2hk', 's2t', 's2tw', 's2twp', 't2hk', 't2s', 't2tw', 'tw2s', 'tw2sp'
    ]

    def cc(self, mode: click.Choice(_cc_modes)):
        from opencc import OpenCC
        instance = OpenCC(mode)
        for line in self._read():
            click.echo(instance.convert(line))

    def charcode(self):
        '''get char code from stdin.'''
        for line in self._read():
            click.echo(','.join([str(ord(ch)) for ch in line]))

    def prfmt(self, pattern):
        '''
        <POWER!> format input using the PATTERN.

        try: `ping 192.168.1.1 | str each prfmt "[{time}] [{index}] {line}"`
        '''
        from .util_prfmt import ContextMapping
        ctxm = ContextMapping()
        for index, line in enumerate(self._read()):
            ctxm.set_index(index)
            ctxm.set_line(line)
            click.echo(pattern.format_map(ctxm))


class StrApp(CommonApp):

    def _read_core(self):
        return [sys.stdin.read()]

    class Each(CommonApp):
        '''work with each line as a standalone str'''
        def _read_core(self):
            for line in sys.stdin:
                if line.endswith('\n'):
                    line = line[:-1]
                yield line

    class Line(BaseApp):
        '''work with the lines collection'''

        def _read_core(self):
            return sys.stdin.read().splitlines()

        def count(self):
            '''show total lines count.'''
            click.echo(len(self._read()))

        def join(self, spliter: str):
            '''join lines by spliter.'''
            click.echo(spliter.join(self._read()))

        def pprint(self, format: str='[{}] ', start: int=0):
            '''pretty print'''
            lines = list(self._read())
            mw = len(str(len(lines) + start))
            for index, line in enumerate(lines):
                idxstr = str(index + start)
                idxstr = idxstr.rjust(mw)
                idxstr = click.style(
                    format.format(idxstr), fg='green'
                )
                msg = f'{idxstr} {line}'
                click.echo(msg)

        def skip_empty(self):
            '''ignore all empty line.'''
            for line in self._read():
                if line:
                    click.echo(line)

        def skip_whitespace(self):
            '''ignore all whitespace line.'''
            for line in self._read():
                if line.strip():
                    click.echo(line)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        app = click_app(allow_inherit=True)(StrApp)
        if sys.stdin.isatty():
            click.echo(
                click.style(
                    'You must call this script use pipe.', fg='red'
                )
            )
            click.echo('   For example:')
            script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
            click.echo(
                click.style(
                    f'      dir | {script} ...', fg='green'
                )
            )
            click.echo()
        app()
    except Exception: # pylint: disable=W0703
        traceback.print_exc()
