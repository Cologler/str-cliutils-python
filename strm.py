#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys
import traceback

from _core import (
    ISession,
    builder,
    execute
)

@builder.command
def join(session: ISession, spliter: str):
    '''join lines by spliter.'''
    print(spliter.join(session.read()))

@builder.command
def insert_linenumber(session: ISession, format: str='[{}] ', start: int=1):
    '''insert line number to line begin for each lines.'''
    lines = session.read()
    mw = len(str(len(lines) + start - 1))
    for index, line in enumerate(lines):
        idxstr = str(index + start - 1)
        idxstr = idxstr.rjust(mw)
        print(format.format(idxstr), line)


@builder.command
def skip_empty(session: ISession):
    '''ignore all empty line.'''
    for line in session.read():
        if line:
            print(line)

@builder.command
def skip_whitespace(session: ISession):
    '''ignore all whitespace line.'''
    for line in session.read():
        if line.strip():
            print(line)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        execute(argv, lambda: sys.stdin.read().splitlines())
    except Exception:
        traceback.print_exc()
        input()

if __name__ == '__main__':
    main()