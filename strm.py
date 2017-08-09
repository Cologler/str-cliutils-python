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