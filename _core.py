#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# 
# ----------

import sys

from jasily.console.commands import CommandManager
from jasily.console.commands import CommandRunningError
from jasily.console.commands import enable_sorted_args
from jasily.console.commands import arg_alias

CM = CommandManager()

def read_from_session(session):
    return session.env['reader']()

@arg_alias(from_right='r')
@enable_sorted_args
@CM.command()
def skip(session, length: str, from_right=False):
    if not length.isdigit():
        raise CommandRunningError('LENGTH should be number.')
    length = int(length)
    for line in read_from_session(session):
        if len(line) <= length:
            print('')
        elif from_right:
            print(line[:len(line) - length])
        else:
            print(line[length:])

@arg_alias(from_right='r')
@enable_sorted_args
@CM.command()
def take(session, length: str, from_right=False):
    if not length.isdigit():
        raise CommandRunningError('LENGTH should be number.')
    length = int(length)
    for line in read_from_session(session):
        if len(line) <= length:
            print(line)
        elif from_right:
            print(line[len(line) - length:])
        else:
            print(line[:length])

def execute(argv, reader):
    if sys.stdin.isatty():
        print('you must call this script use pipe.')
        CM.print_commands()
    else:
        CM.execute(argv, reader=reader)