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
    if sys.stdin.isatty():
        print('You must call this script use pipe. For example:')
        script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
        print('   dir | %s' % script)
        print()
        self.usage()
        return []
    else:
        return self.state['reader']()

ISession.read = read

LEN = len
@builder.command
def len(session: ISession):
    '''get len of str from stdin.'''
    for line in session.read():
        print(LEN(line))
len = LEN

@builder.command
def skip(session: ISession, length: int, from_right=False):
    '''skip number of char from stdin.'''
    for line in session.read():
        if len(line) <= length:
            print('')
        elif from_right:
            print(line[:len(line) - length])
        else:
            print(line[length:])

@builder.command
def take(session: ISession, length: int, from_right=False):
    '''take number of char from stdin.'''
    for line in session.read():
        if len(line) <= length:
            print(line)
        elif from_right:
            print(line[len(line) - length:])
        else:
            print(line[:length])

RANGE = range
@builder.command
def range(session: ISession, start: int, end: int):
    '''same as python str[START:END].'''
    for line in session.read():
        val = line[start: end]
        print(val)
range = RANGE

@builder.command
def char(session: ISession, index: int):
    '''get char by index from stdin.'''
    for line in session.read():
        try:
            val = line[index]
        except IndexError:
            val = ''
        print(val)

@builder.command
def index_of(session: ISession, value: str):
    '''find index of value from stdin.'''
    for line in session.read():
        print(line.find(value))

@builder.command
def replace(session: ISession, old, new):
    '''replace from OLD to NEW.'''
    for line in session.read():
        print(line.replace(old, new))

@builder.command
def insert(session: ISession, value, index: int=0):
    '''insert into source.'''
    for line in session.read():
        if len(line) <= index:
            line = line.ljust(index)
        line = line[:index] + value + line[index:]
        print(line)

@builder.command
def upper(session: ISession):
    '''to upper case.'''
    for line in session.read():
        print(line.upper())

@builder.command
def lower(session: ISession):
    '''to lower case.'''
    for line in session.read():
        print(line.lower())

@builder.command
def split(session: ISession, spliter: str, end: str=None):
    '''split value by spliter.'''
    for line in session.read():
        for x in line.split(spliter):
            print(x)
        if end != None:
            print(end)

@builder.command
def regex(session: ISession, pattern: str, r=None):
    '''replace value from stdin by regex.'''
    try:
        regexp = re.compile(pattern)
    except Exception:
        raise RuntimeException('invalid regex.')
    if r is None:
        r = '{0}'
    for line in session.read():
        match = regexp.search(line)
        if match is None:
            continue
        gs = [match.group(0)] + list(match.groups())
        try:
            print(r.format(*gs))
        except IndexError as err:
            raise RuntimeException(str(err))

OpenCC = None

def cc(session: ISession, mode):
    from opencc import OpenCC
    instance = OpenCC(mode)
    for line in session.read():
        print(instance.convert(line))

@builder.command
def s2t(session: ISession):
    '''convert from Simplified Chinese to Traditional Chinese'''
    cc(session, 's2t')

@builder.command
def s2tw(session: ISession):
    '''convert from Simplified Chinese to TaiWan Traditional Chinese'''
    cc(session, 's2tw')

@builder.command
def t2s(session: ISession):
    '''convert from Simplified Chinese to Traditional Chinese'''
    cc(session, 't2s')

@builder.command
def tw2s(session: ISession):
    '''convert from Simplified Chinese to TaiWan Traditional Chinese'''
    cc(session, 'tw2s')

@builder.command
def charcode(session: ISession):
    '''get char code from stdin.'''
    for line in session.read():
        print(','.join([str(ord(ch)) for ch in line]))


def execute(argv, reader):
    builder.build().execute(argv, state={
        'reader': reader
    })

