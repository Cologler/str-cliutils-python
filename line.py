#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import sys
import traceback
import re

from jasily.cli import EngineBuilder

builder = EngineBuilder()

def parse_range(range_str: str):
    if ':' in range_str:
        return [int(x) if x else None for x in range_str.split(':', 2)]
    else:
        return [int(range_str)]

@builder.command
def slice(range: str):
    try:
        ret = parse_range(range)
    except ValueError:
        lines = []
        lines.append('the first line index is 0. examples:')
        lines.append('   2 -> print line 2.')
        lines.append('   2:5 -> print line 2, 3, 4 (total 3 lines).')
        print(''.join(lines))
        return

    source = sys.stdin.read().splitlines()
    if len(ret) == 2:
        if tuple(ret) != (None, None):
            source = source[ret[0]:ret[1]]
        for line in source:
            print(line)
    elif len(ret) == 1:
        line_index = ret[0]
        if len(source) > line_index:
            print(source[line_index])
        else:
            print('')

@builder.command
def ignore(value: str):
    for line in sys.stdin.read().splitlines():
        if line != value:
            print(line)

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        if sys.stdin.isatty():
            print('you must call this script use pipe.')
        else:
            builder.build().execute(argv)
    except Exception:
        traceback.print_exc()
        input()

if __name__ == '__main__':
    main()
