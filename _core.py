#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import sys
import re

from jasily.cli import (
    EngineBuilder,
    ISession,
    RuntimeException
)

builder = EngineBuilder()

def read(self: ISession):
    return self.state['reader']()
ISession.read = read

LEN = len
@builder.command
def len(session: ISession):
    '''get len of str from source.'''
    for line in session.read():
        print(LEN(line))
len = LEN

@builder.command
def skip(session: ISession, length: int, from_right=False):
    '''skip number of char from source.'''
    for line in session.read():
        if len(line) <= length:
            print('')
        elif from_right:
            print(line[:len(line) - length])
        else:
            print(line[length:])

@builder.command
def take(session: ISession, length: int, from_right=False):
    '''take number of char from source.'''
    for line in session.read():
        if len(line) <= length:
            print(line)
        elif from_right:
            print(line[len(line) - length:])
        else:
            print(line[:length])

@builder.command
def index_of(session: ISession, value: str):
    '''find index of value from source.'''
    for line in session.read():
        print(line.find(value))

@builder.command
def regex(session: ISession, pattern: str, r=None):
    '''replace value from source by regex.'''
    try:
        regex = re.compile(pattern)
    except Exception:
        raise RuntimeException('invalid regex.')
    if r is None:
        r = '{0}'
    for line in session.read():
        match = regex.search(line)
        if match is None:
            continue
        gs = [match.group(0)] + list(match.groups())
        try:
            print(r.format(*gs))
        except IndexError as err:
            raise RuntimeException(str(err))


def execute(argv, reader):
    if sys.stdin.isatty():
        script = os.path.splitext(os.path.basename(argv[0]))[0]
        print('You must call this script use pipe. For example:')
        print('   dir|%s' % script)
    else:
        builder.build().execute(argv, state={
            'reader': reader
        })
